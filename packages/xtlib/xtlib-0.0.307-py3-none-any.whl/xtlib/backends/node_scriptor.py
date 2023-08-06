# node_scriptor.py: builds the script to be run on a node
import os

from xtlib import constants
from xtlib import scriptor
from xtlib import file_utils
from xtlib import utils
from xtlib import store_utils
from xtlib import run_errors
from xtlib import console

from xtlib.helpers import xt_config
from xtlib.backends.mount_helper import MountHelper
from xtlib.backends.cmd_appender import CmdAppender
from xtlib.backends.backend_base import BackendBase

def join(p1, p2):
    # ensure unix path results
    return p1 + "/" + p2

class NodeScriptor():
    '''
    Created on Mar-24-2023 to refactor the "script wrapping" code spread out over backend_base.py and all other backend classes.

    Builds the script to be run on each node of a job.  Assumptions:

        - user and XT environment variables are set by the backend
    
        - runtime script parameters are provided in the form of environment variables.

        - support for windows compute nodes has been removed (script will only run on linux boxes)
    '''

    def __init__(self, cwd:str, controller_cmd:str, manual_docker:bool, 
            compute_def, mount_helper:MountHelper, backend:BackendBase, homebase="$HOME", 
            mountbase="$HOME", tmpbase="$HOME", use_sudo=False, 
            default_docker_image=None, get_env_vars_from_file=False, config=None, args=None) -> None:
        '''
        Args:
            - cwd: the working directory for the controller

            - homebase: the base directory used to build:
                - controller working dir   (homebase/.xt/cwd)
                - mounting paths (homebase/.xt/mnt/xxx)
                - local data paths (homebase/.xt.local/xxx)

            - controller_cmd: the command to run the controller
        '''

        self.cwd = cwd
        self.controller_cmd = controller_cmd
        self.manual_docker = manual_docker
        self.backend = backend
        self.backend_name = backend.get_name()
        self.compute_def = compute_def
        self.mount_helper = mount_helper
        self.use_sudo = use_sudo
        self.default_docker_image = default_docker_image
        self.get_env_vars_from_file = get_env_vars_from_file
        self.config = config
        self.args = args

        self.homebase = homebase
        self.mountbase = mountbase
        self.tmpbase = tmpbase

        setup_name = compute_def["setup"]
        setup = self.config.get_setup_from_target_def(compute_def, setup_name)

        self.pre_setup_cmds = utils.safe_value(setup, "pre-cmds", None)
        self.post_setup_cmds = utils.safe_value(setup, "post-cmds", None)
        self.mounting_enabled = utils.safe_value(setup, "mounting-enabled")

        self.bootstrap_dir = args["bootstrap_dir"]
        self.docker_name = utils.safe_value(compute_def, "docker")    # args["docker"]

        # scripting options
        self.log_reports = args["log_reports"]
        self.db_reports = True      # TODO: make this a config file option

        # TODO: property apply use_sudo (right now its hard-coded throughout this class)

        # share a single CmdAppender instance to keep thihgs in sync
        self.ca = mount_helper.ca

    def generate_script(self):
        '''
        Generates the node script and writes it to FN_NODE_SCRIPT.  
        If manual_docker is True, it will also generate an inner script: FN_INNER_SCRIPT.
        '''
        # generate the main setup/run script
        cmds = self.ca.init_cmds()
        context = self.get_primary_context()
        self.ca.set_context(context)

        # generate the MAIN node script
        self.gen_primary_script(cmds, set_xt_started=(not self.manual_docker))

        if self.manual_docker:
            # we need to generate a docker node script (that will run the main node script)
            fn_inner = self.write_cmds_to_file(constants.FN_INNER_SCRIPT, cmds)

            docker_cmds = self.ca.init_cmds()
            self.ca.set_context("before docker")

            self.gen_first_cmds(docker_cmds, set_xt_started=True)
            self.gen_system_reports(docker_cmds)
            fn_pull = self.gen_docker_run(docker_cmds)

            fn_node_script = self.write_cmds_to_file(constants.FN_NODE_SCRIPT, docker_cmds)

        else:
            fn_inner = None
            fn_pull = None
            fn_node_script = self.write_cmds_to_file(constants.FN_NODE_SCRIPT, cmds)

        # copy generated files to home dir
        dir_name = file_utils.get_xthome_dir()
        self.copy_file_to_dir(fn_node_script, dir_name)

        if fn_inner:
            self.copy_file_to_dir(fn_inner, dir_name)

        if fn_pull:
            self.copy_file_to_dir(fn_pull, dir_name)

        return fn_node_script, fn_inner

    def get_primary_context(self):

        if self.manual_docker:
            context = "inside docker"
        else:
            if self.docker_name:
                context = "inside docker"
            else:
                context = "native"

        return context

    def copy_file_to_dir(self, fn, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(fn, "rt") as f:
            text = f.read()

        fn_out = join(dir, os.path.basename(fn))
        with open(fn_out, "wt") as f:
            f.write(text)

    def gen_primary_script(self, cmds, set_xt_started):

        self.gen_first_cmds(cmds, set_xt_started)
        self.gen_system_reports(cmds)

        self.gen_run_prep(cmds)
        self.gen_run(cmds)
        self.gen_run_post(cmds)

    def gen_run_prep(self, cmds):
        self.gen_prep_code_and_working_dir(cmds)
        self.gen_package_setup(cmds)

        # generate all of the blobfuse/mount commands
        self.mount_helper.gen_mount_and_download_cmds(cmds)

    def is_using_docker(self):
        docker_name = self.args["docker"]
        using_docker = bool(docker_name)

        # docker_image, login_server, docker_registry, _ = self.config.get_docker_info(target, docker_name, required=False) 
        # using_docker = bool(docker_image)       

        return using_docker
    
    def gen_prep_code_and_working_dir(self, cmds):
        '''
        The code files (CODE_ZIP_FN or *.*) are in the current directory.
        '''
        using_docker = self.is_using_docker()
        self.backend.gen_code_prep_cmds(self.ca, cmds, self.cwd, using_docker)

        # cwd = self.cwd
        # code_dir = self.code_dir
        # is_code_zipped = self.is_code_zipped

        # cwd = file_utils.fix_slashes(cwd, is_linux=True, protect_ws_run_name=False)
        # fn_code = join(code_dir, constants.CODE_ZIP_FN)

        # if is_code_zipped:
        #     # UNZIP bootstrap and code files from code_dir to cwd
        #     self.ca.append_title(cmds, "UNZIP code from code_dir to cwd:")
        #     self.append_unzip(cmds, fn_code, cwd)

        #     if code_dir == ".":
        #         # remove the .zip file (to keep future copies faster)
        #         self.ca.append(cmds, "rm {}".format(constants.CODE_ZIP_FN))

        # elif cwd != ".":
        #     # COPY bootstrap files from code_dir to cwd
        #     # UNZIP code files to cwd
        #     cwd = file_utils.fix_slashes(cwd, is_linux=True, protect_ws_run_name=False)

        #     self.ca.append_title(cmds, "COPY code files from code_dir to cwd:")
        #     self.ca.append(cmds, "mkdir -p {}".format(cwd))
        #     self.ca.append(cmds, "cp -r {}/. {}".format(code_dir, cwd))

        #     # unzip code
        #     self.append_unzip(cmds, fn_code, cwd)

        # if cwd != ".":
        #     self.ca.append(cmds, "cd {}".format(cwd))

        self.ca.append(cmds, 'echo current dir: {}'.format("$PWD"), echo=False)
        self.ca.append_dir(cmds, ".")

        # now that we have moved to the CWD, we can create the "inside docker or native" __AFTER__ dir
        self.ca.append(cmds, "mkdir -p {}".format(constants.LINUX_AFTER_LOGS))


    def gen_docker_run(self, cmds):
        # prep node for docker run

        self.ca.append_title(cmds, "PREP node for docker run:")

        # ensure docker is installed and running
        install_docker = utils.safe_value(self.compute_def, "install-docker")
        if install_docker:
            # host OS doesn't have docker, so we must install it

            # snap install has problem reading the --env-file (gets permission denied)
            # self.ca.append(cmds, "sudo snap install docker")
            # self.ca.append(cmds, "sudo snap start docker")

            # self.ca.append(cmds, "nvcc --version")
            # self.ca.append(cmds, "sudo docker run hello-world", log="hello-world.log")

            self.ca.append(cmds, "curl -fsSL https://get.docker.com -o get-docker.sh")
            self.ca.append(cmds, "sudo sh ./get-docker.sh")

            # ensure docker is functional
            self.ca.append(cmds, "sudo docker run hello-world", log="hello-world.log")

        else:
            # host OS already has docker installed
            self.ca.append(cmds, "sudo service docker start ") 

        # do we need to move docker files?
        if self.backend_name == "batch":
            azure_image = utils.safe_value(self.compute_def, "azure-image")
            img_dict = self.config.get("azure-batch-images", azure_image)
            mount_docker = utils.safe_value(img_dict, "mount-docker")
            if mount_docker:
                # move docker files to specified mount point (for nodes where system storage is too small for our docker image)

                docker_path = utils.safe_value(img_dict, "docker-path")
                if not docker_path:
                    docker_path = "/var/lib/docker"

                self.ca.append_title(cmds, "MOVE docker files to mount point: {}".format(mount_docker))
                self.ca.append(cmds, "sudo systemctl stop docker")
                self.ca.append(cmds, "sudo mv {} {}-backup".format(docker_path, docker_path))
                self.ca.append(cmds, "sudo mkdir -p {}".format(docker_path))

                self.ca.append(cmds, "sudo mount {} {}".format(mount_docker, docker_path))
                self.ca.append(cmds, "sudo cp -rf {}-backup/. {}".format(docker_path, docker_path))
                self.ca.append(cmds, "sudo systemctl start docker")

                # ensure docker is functional
                self.ca.append(cmds, "sudo docker run hello-world", log="hello-world.log")

        # transfer the XT_ env vars to the docker environment by appending them to the env var file
        fn_env_var = constants.FN_DOCKER_ENV
        self.ca.append(cmds, "printenv | grep XT_ >> {}".format(fn_env_var))
        #self.ca.append(cmds, "cat {}".format(fn_env_var))

        self.ca.append_dir(cmds)

        docker_run_cmd = utils.safe_value(self.compute_def, "docker-run-cmd")
        if docker_run_cmd:
            docker_name = docker_run_cmd.split()[0]
            self.ca.append_export(cmds, "DOCKER_NAME", "{}".format(docker_name))
            self.ca.append_export(cmds, "DOCKER_RUN", "{}".format(docker_run_cmd))

        else:
            # we use DOCKER_NAME for the pull and test
            # we use DOCKER_RUN for the actual run (docker cmd references $DOCKER_RUN)
            self.ca.append_title(cmds, "Determine which docker to use:")

            self.ca.append(cmds, 'test $(which nvidia-docker) && export DOCKER_RUN="nvidia-docker run"' + 
                ' || export DOCKER_RUN="docker run --gpus all"')

            self.ca.append(cmds, 'test $(which nvidia-docker) && export DOCKER_NAME="nvidia-docker"' + 
                ' || export DOCKER_NAME="docker"')

            self.ca.append(cmds, 'echo "DOCKER_NAME: $DOCKER_NAME"', echo=False)
            self.ca.append(cmds, 'echo "DOCKER_RUN: $DOCKER_RUN"', echo=False)

        fn_pull = self.gen_docker_pull_and_run(cmds)

        # how is this file used?
        docker_name = self.args["docker"]   # self.docker_name
        self.write_docker_info_file(docker_name)

        return fn_pull

    def gen_docker_pull_and_run(self, cmds):

        self.export_now_to_var(cmds, "XT_PULL_START_TIME")
        fn_pull = None

        timeout = self.args["docker_pull_timeout"]
        login_cmd = self.args["docker_login_cmd"]
        docker_cmd = self.args["docker_cmd"]
        image_name = self.args["full_docker_image"]

        if timeout:
            #sudo = "sudo " # if sudo_available else ""

            pull_cmds = self.ca.init_cmds()

            self.ca.append_title(pull_cmds, "DOCKER PULL ATTEMPT", double=True)

            # restart docker service
            self.ca.append(pull_cmds, "echo restarting docker service...", echo=False)
            self.ca.append(pull_cmds, "sudo systemctl daemon-reload")
            self.ca.append(pull_cmds, "sudo systemctl restart docker")

            # pull docker image
            self.gen_pull_core(pull_cmds, image_name, login_cmd)

            # # test docker image by running XT with minimum command
            # self.ca.append(pull_cmds, "echo testing docker image by running 'xt --version' within it...", echo=False)
            # self.ca.append(pull_cmds, "sudo $DOCKER_NAME run --rm {} xt --version".format(image_name))

            self.ca.append_title(cmds, "TESING DOCKER IMAGE")
            # test docker image by running a simple cmd within it (ls -lt)
            self.ca.append(pull_cmds, "echo testing docker image by running 'ls -lt' within it...", echo=False)
            self.ca.append(pull_cmds, "sudo $DOCKER_NAME run --rm {} ls -lt".format(image_name), log="docker_pull_test.log")

            # write PULL CMDS to FN_DOCKER_PULL_SH
            fn_pull = self.write_cmds_to_file(constants.FN_DOCKER_PULL_SH, pull_cmds)
            utils.copy_to_submit_logs(self.args, fn_pull)

            pull_retry_cmd = '''timeout {} bash -c "until bash {}; do '''.format(timeout, constants.FN_DOCKER_PULL_SH) + \
                '''echo XT: docker pull+test failed.  retrying...; sleep 60; done" '''

            self.ca.append(cmds, pull_retry_cmd)
            self.ca.append(cmds, "docker_pull_status=$?", echo=True)
            self.ca.append(cmds, "if [ $docker_pull_status -ne 0 ]; then", echo=False)
            self.ca.append(cmds, 'echo "XT: ERROR - docker pull TIMED OUT; job aborted"', echo=False)
            self.ca.append(cmds, "else", echo=False)
            self.ca.append(cmds, 'echo "XT: docker pull+test SUCCEEDED!"', echo=False)

            # run the node script with docker
            self.ca.append_title(cmds, "DOCKER RUN:")
            self.ca.append(cmds, docker_cmd)
            self.ca.append(cmds, "fi", echo=False)

        else:
            # not using TIMEOUT option
            self.gen_pull_core(cmds, image_name, login_cmd)

            # run the node script with docker
            self.ca.append_title(cmds, "DOCKER RUN:")
            self.ca.append(cmds, docker_cmd)

        return fn_pull

    def gen_pull_core(self, cmds, image_name, login_cmd):
        if login_cmd:
            self.ca.append_title(cmds, "DOCKER LOGIN:")
            self.ca.append(cmds, login_cmd)

        self.ca.append_title(cmds, "DOCKER PULL:")
        capture_pull = self.config.get("logging", "capture-docker-pull")

        # do an explict pull of the docker image
        if capture_pull:
            self.ca.append(cmds, "echo pulling docker image \(pull output being captured\)...", echo=False)
            self.ca.append(cmds, "sudo $DOCKER_NAME pull {}".format(image_name), log="docker_pull")
        else:
            self.ca.append(cmds, "sudo $DOCKER_NAME pull {}".format(image_name))

    def write_docker_info_file(self, docker_name):

        # finally, write the full name of the docker image to a special file to be included in the bootstrap files
        fn_image = join(self.bootstrap_dir, constants.FN_IMAGE_NAME)
        target = self.args["target"]

        docker_image, login_server, _, _ = self.config.get_docker_info(target, docker_name, required=False)
        full_image_name = login_server + "/" + docker_image  if login_server else docker_image

        file_utils.write_text_file(fn_image, full_image_name)


    def gen_package_setup(self, cmds):

        pip_freeze = self.args["pip_freeze"]

        if pip_freeze:
            self.ca.append_title(cmds, "PRE-SETUP PIP FREEZE")
            self.ca.append(cmds, "pip freeze", log="final_pip_freeze")

        if self.pre_setup_cmds:
            self.add_user_cmds(cmds, self.pre_setup_cmds, "PRE-SETUP")

        conda_packages = self.args["conda_packages"]
        pip_packages = self.args["pip_packages"]

        if conda_packages or pip_packages:
            self.ca.append_title(cmds, "PACKAGE SETUP")

            # CONDA packages
            if conda_packages:
                self.add_conda_packages(cmds, conda_packages)
            
            # PIP packages
            if pip_packages:
                use_legacy_resolver = self.args["use_legacy_resolver"]
                self.add_pip_packages(cmds, pip_packages, use_legacy_resolver)

        if self.post_setup_cmds:
            self.add_user_cmds(cmds, self.post_setup_cmds, "POST-SETUP")

        if pip_freeze:
            self.ca.append_title(cmds, "POST-SETUP PIP FREEZE")
            self.ca.append(cmds, "pip freeze", log="final_pip_freeze")

        self.add_xt_setup_cmds(cmds)

        self.framework_report(cmds)
        self.xt_report(cmds)

    def add_conda_packages(self, cmds, conda_packages):
        cmd = "conda install"
        # NOTE: double quotes around package names cause error on linux
        for cp in conda_packages:
            cmd += ' {}'.format(cp)
        self.ca.append(cmds, cmd, log="conda_install")

    def add_pip_packages(self, cmds, pip_packages, use_legacy_resolver=False):
        cmd = "pip install --user"
        if use_legacy_resolver:
            cmd += " --use-deprecated=legacy-resolver"

        # NOTE: double quotes around package names cause error on linux
        for pp in pip_packages:
            cmd += ' {}'.format(pp)
        self.ca.append(cmds, cmd, log="pip_install")
            
    def add_xt_setup_cmds(self, cmds):
        # add "." to PYTHONPATH so that any run of xt.exe will pick up latest XTLIB and USER LIBS
        pp = self.args["python_path"]     # a list of strings from SETUP in config file

        if not pp:
            # by default, we add XT_CWD to path so xtlib and other libraries usually just work
            self.ca.append_export(cmds, "PYTHONPATH", "$XT_CWD")
        else:
            # user has specified the PYTHONPATH; give them complete control
            pp_str = ":".join(pp)
            path = file_utils.fix_slashes(pp_str, is_linux=True, protect_ws_run_name=False)
            self.ca.append_export(cmds, "PYTHONPATH", path)

        self.add_python_path(cmds)
        
    def add_user_cmds(self, cmds, user_cmds, name):
        self.ca.append_title(cmds, "USER {} commands:".format(name))

        for cmd in user_cmds:
            self.ca.append(cmds, cmd, echo="old_style")

        # sync up command echo with append system
        self.ca.sync_trace(cmds, True)

        # restore the working dir
        self.ca.append(cmds, "cd $XT_CWD")

    def gen_run(self, cmds):
        # debug
        self.ca.append_dir(cmds)

        is_direct_run = self.config.get("general", "direct-run")
        if is_direct_run:
            self.ca.append_title(cmds, "LAUNCHING USER SCIPT (direct-run=1):")
            
            working_dir = self.args["working_dir"]
            if working_dir:
                self.ca.append(cmds, "cd {}".format(working_dir))

            self.ca.append(cmds, "echo XT_DIRECT_CMD is $XT_DIRECT_CMD")

            # run direct cmd
            self.ca.append(cmds, "$XT_DIRECT_CMD")
            
            self.ca.append_title(cmds, "DIRECT CMD EXITED:")

        else:
            self.ca.append_title(cmds, "LAUNCHING XT CONTROLLER:")
            self.ca.append(cmds, self.controller_cmd)
            self.ca.append_title(cmds, "XT CONTROLLER EXITED:")

    def gen_run_post(self, cmds):
        self.export_now_to_var(cmds, "XT_POST_START_TIME")

        self.ca.append_dir(cmds, ".")

        self.gen_log_upload_cmds(cmds)

        self.gen_unmount_cmds(cmds)

        # log the POST end_time and duration using the xtlib node_post_wrapup.py script
        cmd = 'python -c "from xtlib import node_post_wrapup; node_post_wrapup.main()" '
        self.ca.append(cmds, cmd)

        self.add_node_sleep_cmd(cmds)

        #self.ca.append(cmds, ":")     # one last command to give us a timestamp for exit
        self.ca.append_title(cmds, 'END of XT-level processing', double=True)

    def add_node_sleep_cmd(self, cmds):
        sleep_on_exit = self.args["sleep_on_exit"]
    
        if sleep_on_exit:
            secs = utils.shell_time_str_to_secs(sleep_on_exit)
            if secs > 0:
                self.ca.append_title(cmds, 'sleeping on exit...')
                self.ca.append(cmds, "sleep {}".format(sleep_on_exit))

    def gen_log_upload_cmds(self, cmds):
        '''
        We try to not rely on xtlib being installed in the wrapper script so that
        the user can access and view logs about problems he may have installing 
        xtlib.  
        '''

        self.ca.append_title(cmds, "UPLOAD service and XT logs to job storage:")
        args = self.args

        # workaround for "$jobs" not resolving correctly on compute node
        job_id = args["job_id"]
        workspace = args["workspace"]
        jobs_container = store_utils.get_jobs_container(workspace)

        # copy from __after__/xt_logs to output node dir
        dest = "$XT_NODE_DIR/after/xt_logs"
        self.ca.append(cmds, "mkdir -p {}".format(dest))
        self.ca.append(cmds, "cp -r {}/. {}".format(constants.LINUX_AFTER_LOGS, dest))

        if self.manual_docker:
            self.ca.append(cmds, "cp -r /usr/src/{}/. {}".format(constants.LINUX_AFTER_LOGS, dest))

        # copy node run_errors directory to output node dir (but avoid err msg if no files)
        dest = "$XT_NODE_DIR/after/run_errors"
        cmd = "find {}/. > /dev/null 2>&1 && mkdir -p {} && cp -r {}/. {}".format( \
            run_errors.LINUX_RUN_ERRORS_DIR, dest, run_errors.LINUX_RUN_ERRORS_DIR, dest)
        self.ca.append(cmds, cmd)

        dest = "$XT_NODE_DIR/after/service_logs"
        # have backend add its needed cmds to copy the service logs
        self.ca.sync_trace(cmds, True)      # turn on echo for following cmds
        self.backend.add_service_log_copy_cmds(self.ca, cmds, dest, args)         
        self.ca.sync_trace(cmds, True)      # turn on echo for following cmds

        # if jobs_container was not mounted thru blobfuse, use XT to manually upload the files
        if not self.mounting_enabled:
            job_id = self.args["job_id"]
            store_after = "/{}/jobs/{}/nodes/node$XT_NODE_INDEX/after".format(jobs_container, job_id)
            # if blobfuse is unavailable, we manually upload the logs using XT (assumes XT has been successfully loaded)
            src_after = "$XT_NODE_DIR/after"
            cmd = "xt upload {} {} --feedback=0".format(src_after, store_after)

            # NOTE: this "xt upload" cmd will not appear the log for pool jobs (since it is capturing the log at this point in time)
            # However: all messages should appear in the "xt monitor" output of a live job
            # The service logs collected by Batch and AML jobs should always include this cmd.
            self.ca.append(cmds, cmd, echo=True)

    def gen_unmount_cmds(self, cmds):
        # remove all mounted drives
        self.mount_helper.gen_unmount_all(cmds)

    def gen_first_cmds(self, cmds, set_xt_started):

        # we must set XT_STARTED before we can print the context in append_title()
        self.ca.append_title(cmds, 'START of XT-level processing', double=True, zero_duration=set_xt_started)

        if set_xt_started:
            self.ca.append_export(cmds, "XT_STARTED", "$(date +%s)", echo=False)
            self.ca.append(cmds, 'echo "Node started: $(date)"', echo=False)
            self.set_xt_started = True

        # make a directory for the XT logs (we may need to make again if CWD is changed)
        self.ca.append(cmds, "mkdir -p {}".format(constants.LINUX_AFTER_LOGS))

        self.gen_sleep_cmd(cmds)
        #self.log_batch_debug(cmds)

        self.ca.append(cmds, "echo 'User environment variables specified in the XT config file are predefined in this shell.'", echo=False)

        self.gen_shared_env_vars(cmds)

        self.gen_starting_environment_report(cmds)

        if self.report_filter("vars"):
            # XT ENV VAR report
            self.ca.append_title(cmds, "XT Environment variable report:")
            self.ca.append(cmds, 'printenv | grep "^XT_"', echo=False)

        # # debug
        # self.ca.append_dir(cmds)

    def report_filter(self, name):
        found = ("all" in self.log_reports) or (name in self.log_reports)
        return found

    def gen_starting_environment_report(self, cmds):

        if self.report_filter("start"):
            self.ca.append_title(cmds, "STARTING environment report:", echo=False)

            target = self.args["target"]
            docker_name = self.args["docker"]
            docker_image, login_server, docker_registry, _ = self.config.get_docker_info(target, docker_name, required=False)
            docker_image = login_server + "/" + docker_image if login_server else docker_image

            if not docker_image:
                docker_image = self.default_docker_image

            job_id = self.args["job_id"]
            node_info = self.config.get_target_desc_from_def(target, self.backend_name, self.compute_def)
            node_info = node_info.replace("target=", "")

            self.add_info(cmds, "job id", job_id)
            self.add_info(cmds, "node id", "$XT_NODE_ID")
            self.add_info(cmds, "run name", "$XT_RUN_NAME")
            self.add_info(cmds, "target", node_info)
            self.add_info(cmds, "hostname", "$(hostname)", "%COMPUTERNAME%")

            self.add_info(cmds, "IP address", "$(hostname -I | awk '{print $2}')")
            self.add_info(cmds, "OS version", '''$(cat /etc/os-release | grep PRETTY_NAME | cut -d '"' -f2)''')
            self.add_info(cmds, "Conda env", "$CONDA_DEFAULT_ENV", "%CONDA_DEFAULT_ENV%")
            self.ca.append(cmds, "if [ -f /.dockerenv ]; then export IN_DOCKER=True; else export IN_DOCKER=False; fi")
            self.add_info(cmds, "In docker", "$IN_DOCKER", "False")
            self.add_info(cmds, "Image request", docker_image)
            self.add_info(cmds, "Image name", "$DOCKER_IMAGE_NAME", "%DOCKER_IMAGE_NAME%")
            self.add_info(cmds, "GPU type", "$(nvidia-smi -L | cut -d'(' -f1)")

            self.add_python_info(cmds)

            # PYTORCH version
            target_cmd = '''python -c "import torch; print('PyTorch:'.ljust(15) + ' ' + torch.__version__)"'''   # .ljust(15)+ ', C
            self.add_package_test(cmds, "torch", target_cmd, "PyTorch")

            # CUDA version
            target_cmd = '''python -c "import torch; print('CUDA version:'.ljust(15) + ' ' + torch.version.cuda)"'''
            self.add_package_test(cmds, "torch", target_cmd, "cuda")

            # CUDA gpu_count
            target_cmd = '''python -c "import torch; print('CUDA gpu_count: '.ljust(15) + str(torch.cuda.device_count()))"'''
            self.add_package_test(cmds, "torch", target_cmd, "PyTorch")

            # CUDA available
            target_cmd = '''python -c "import torch; print('CUDA available: '.ljust(15) + str(torch.cuda.is_available()))"'''
            self.add_package_test(cmds, "torch", target_cmd, "PyTorch")

            self.add_info(cmds, "running", "$(basename $0)", "%0")
            self.add_info(cmds, "current dir", "$(pwd)", "%CD%")
            self.add_info(cmds, "username", "$(whoami)", "%USERNAME%")

            self.ca.append_dir(cmds, ".")

    def gen_sleep_cmd(self, cmds):
        # construct SLEEP CMD to randomly delay start of node execution
        node_count = self.args["node_count"]
        node_delay = self.args["node_delay"]

        if node_delay and node_count > 1:
            value = int(utils.shell_time_str_to_secs(node_delay))
            sleep_cmd = "sleep $((RANDOM % {}))".format(value)
        else:
            sleep_cmd = None

        if sleep_cmd:
            self.ca.append(cmds, sleep_cmd)

    def gen_shared_env_vars(self, cmds):

        self.ca.append_title(cmds, "create shared XT env vars:")
        self.export_now_to_var(cmds, "XT_PREP_START_TIME")

        # remember original dir for service log files at end
        pwd_cmd = "$(pwd)"
        self.ca.append_export(cmds, "XT_ORIG_WORKDIR", pwd_cmd, fix_value=False)

        if self.homebase == ".":
            self.ca.append_export(cmds, "XT_HOMEBASE", pwd_cmd, fix_value=False)
        else:
            self.ca.append_export(cmds, "XT_HOMEBASE", self.homebase, fix_value=False)

        cwd = self.cwd

        if cwd == ".":
            cwd = "$PWD"

        self.ca.append_export(cmds, "XT_CWD", cwd, fix_value=False)

        self.ca.append_export(cmds, "XT_NODE_ID", "node$XT_NODE_INDEX")
        self.ca.append_export(cmds, "XT_MOUNTING_ENABLED", self.mounting_enabled)

        job_id = self.args["job_id"]
        ws_name = self.args["workspace"]
        self.ca.append_export(cmds, "XT_JOB_ID", job_id)
        self.ca.append_export(cmds, "XT_WORKSPACE_NAME", ws_name)

        # for debugging version 1 vs. 2 issues
        self.ca.append_export(cmds, "XT_STORE_NAME", self.config.get("store"))
        self.ca.append_export(cmds, "XT_JOBS_CONTAINER_NAME", store_utils.get_jobs_container(self.args["workspace"]))
        self.ca.append_export(cmds, "XT_STORAGE_FORMAT", store_utils.STORAGE_FORMAT)

        # workaround for Pytorch 1.5/1.6 issue
        # note: this is set in the std xtlib docker files but something in AML must be changing it
        # so we reset it to GNU here (to avoid MKL NOT COMPATIBLE error in AML runs)
        #self.ca.append(cmds, "echo before setting, MKL_THREADING_LAYER is: $MKL_THREADING_LAYER", echo=False)
        self.ca.append_export(cmds, "MKL_THREADING_LAYER", "GNU")

        if self.get_env_vars_from_file:
            # on singularity and pool, we restore long env var strings from a separate script
            self.ca.append(cmds, "export $(cat {} | xargs)".format(constants.FN_SET_ENV_VARS))    

    def log_batch_debug(self, cmds):        
        if self.backend_name == "batch":
            # run script to extract Azure Batch NODE and POOL ids
            # this is done for debugging nodes with Azure Batch team
            ws_id = self.args["workspace"]
            job_id = self.args["job_id"]

            # get BATCH credentials
            service = self.compute_def["service"]
            batch_creds = self.config.get_service(service)
            batch_url = batch_creds["url"]

            batch_job_id = self.make_batch_job_id(ws_id, job_id)

            self.ca.append(cmds, "echo running script to extract Azure Batch NODE and POOL ids", echo=False)
            self.ca.append(cmds, "python {} {} $XT_NODE_INDEX {} {} {}".format(constants.FN_BATCH_NODE_ID, batch_job_id, service, batch_url, "$XT_BATCH_KEY"))

    def gen_system_reports(self, cmds):

        if self.report_filter("os"):
            # OS report
            self.ca.append_title(cmds, "OS report:")
            self.ca.append(cmds, "cat /etc/os-release")
            self.ca.append(cmds, "cat /etc/motd")
            self.ca.append(cmds, "whoami")

        if self.report_filter("package"):
            # Python package report
            self.ca.append_title(cmds, "Package report:")
            self.ca.append(cmds, "pip list")

        if self.report_filter("disk"):
            # Disk report
            self.ca.append_title(cmds, "Disk report:")
            self.ca.append(cmds, "df -h")

        if self.report_filter("memory"):
            # Memory report
            self.ca.append_title(cmds, "MEMORY report:")
            self.ca.append(cmds, "free -mh")

        if self.report_filter("cpu"):
            # CPU report
            self.ca.append_title(cmds, "CPU report:")
            self.ca.append(cmds, "lscpu")

        if self.report_filter("gpu"):
            # GPU report
            self.ca.append_title(cmds, "GPU report:")
            # several techinques to show version of NVIDIA DRIVERS
            self.ca.append(cmds, "whereis nvidia")
            # debug nvidia drivers/toolkit combinations
            self.ca.append(cmds, "nvidia-smi")

    def write_cmds_to_file(self, fn, cmds):
        fn_path = self.bootstrap_dir + "/" + fn
        scriptor.write_script_file(cmds, fn_path, False)
        utils.copy_to_submit_logs(self.args, fn_path)

        return fn_path

    def export_now_to_var(self, cmds, var_name):
        '''
        export current date/time in an arrow-compatible format, including timezone, to specified var_name.
        '''
        # don't use arrow (early setup - it may not be installed)
        #now_cmd = 'python -c "import arrow; print(arrow.now())"'

        # don't use datetime (early python versions may not support astimezone() with no arg)
        #now_cmd = 'python -c "import datetime; print(datetime.datetime.now().astimezone())"'

        # time gives us pretty much what we need (except for fractions of a second)
        now_cmd = '''python -c "import time; print(time.strftime('%Y-%m-%d %H:%M:%S.0%z', time.localtime()))"'''
        self.ca.append_export(cmds, var_name, '$({})'.format(now_cmd), fix_value=False)

    def make_batch_job_id(self, ws_name, job_id):
        # qualify job_id with store_name and ws_name to minimize duplicate job names
        store_name = self.config.get("store")
        name = "{}__{}__{}".format(store_name, ws_name, job_id)
        return name

    def add_info(self, cmds, title, linux_cmd, windows_cmd=None):

        # expand all titles to same size for uniform columns
        title = (title + ":").ljust(15)

        # these embedded double quotes enable the tab char to be recognized on linux
        cmd = '''echo "{} {}"'''.format(title, linux_cmd)

        self.ca.append(cmds, cmd, echo=False)

    def add_python_info(self, cmds):
        # the "2>&1" is used to join stderr to stdout here (since versions of python use both)
        # cmds.append("python -V > __t__ 2>&1 && xt_tmp=$(cat  __t__)")
        # self.add_info(cmds, "Python", "$xt_tmp")
        self.add_info(cmds, "Python", "$(python -V 2>&1)")

    def framework_report(self, cmds):

        if self.report_filter("framework"):

            self.ca.append_title(cmds, "FRAMEWORK report:", echo=False)

            self.add_python_info(cmds)

            self.add_info(cmds, "Conda env", "$CONDA_DEFAULT_ENV", "%CONDA_DEFAULT_ENV%")
            
            # PYTORCH version
            target_cmd = '''python -c "import torch; print('PyTorch:'.ljust(15) + ' ' + torch.__version__)"'''   # .ljust(15)+ ', C
            self.add_package_test(cmds, "torch", target_cmd, "PyTorch")

            # CUDA version
            target_cmd = '''python -c "import torch; print('CUDA version:'.ljust(15) + ' ' + torch.version.cuda)"'''
            self.add_package_test(cmds, "torch", target_cmd, "cuda")

            # CUDA gpu_count
            target_cmd = '''python -c "import torch; print('CUDA gpu_count: '.ljust(15) + str(torch.cuda.device_count()))"'''
            self.add_package_test(cmds, "torch", target_cmd, "PyTorch")

            # CUDA available
            target_cmd = '''python -c "import torch; print('CUDA available: '.ljust(15) + str(torch.cuda.is_available()))"'''
            self.add_package_test(cmds, "torch", target_cmd, "PyTorch")

            # TORCHVISION
            target_cmd = '''python -c "import torchvision; print('torchvision:'.ljust(15) + ' ' + torchvision.__version__ )"'''
            self.add_package_test(cmds, "torchvision", target_cmd, "torchvision")

            # for now, OMIT tensorflow (can take 30-60 secs to initialize cuda, etc.)
            # # TENSORFLOW
            # target_cmd = '''python -c "import tensorflow as tf; print('Tensorflow:'.ljust(15) + ' ' + tf.__version__ + ', CUDA available: ' + str(tf.test.is_gpu_available()))"'''
            # self.ca.append_package_test(cmds, "tensorflow", target_cmd, "Tensorflow")

    def xt_report(self, cmds):

        if self.report_filter("xt"):
            self.ca.append_title(cmds, "XT report:")
            self.ca.append(cmds, "which xt python conda blobfuse")

            self.ca.append(cmds, "xt --version", echo=True)

    def add_package_test(self, cmds, package_to_import, target_cmd, ni_name):
        nul_name = "/dev/null"

        cond_cmd = '''python -c "import {}" 2>{}'''.format(package_to_import, nul_name)

        # need to surround with double quotes for tab to be recognized
        else_cmd = 'echo "{}: \tnot installed"'.format(ni_name)

        cmd = "{} && {} 2>{}".format(cond_cmd, target_cmd, nul_name)
        cmd2 = "{} || {}".format(cond_cmd, else_cmd)
        self.ca.append(cmds, cmd)
        self.ca.append(cmds, cmd2)

    def add_python_path(self, cmds):
        self.add_info(cmds, "PYTHONPATH", "$PYTHONPATH")


def scriptor_test():
    fn_config = os.path.abspath(os.path.dirname(__file__) + "../../../cmdlineTest/xt_config.yaml")
    config = xt_config.get_merged_config(local_overrides_path=fn_config)

    controller_cmd = "python -u {}".format(constants.PY_RUN_CONTROLLER)
    target = "labcoatbatch-hi"
    compute_def = dict(config.get_target_def(target))
    homebase = "$HOME/.xt"
    mountbase = "$HOME"
    tmpbase = "$HOME"
    actions = ["data", "model"]
    storage_name = "sandboxstoragev2s"
    backend_name = "batch"
    manual_docker = True
    docker_cmd = "docker run -it --rm --gpus all --ipc=host --network=host --privileged hello-world"
    use_sudo = False

    args = dict(bootstrap_dir="/tmp/xt_bootstrap", setup="batchd", log_reports=True, snapshot_dirs=True, capture_setup_cmds=True, 
            node_count=2, node_delay="5s", workspace="ws4", job_id="job1001", 
            target=target, docker="pytorch-xtlib", pip_freeze=True, conda_packages=["torch"], 
            pip_packages=["xtlib"], use_legacy_resolver=True, python_path=None, data_share_path=None, model_share_path=None, 
            data_action="mount", model_action="mount", data_mount_path=None, model_mount_path=None, data_writable=False, 
            model_writable=False, storage=storage_name, mount_retry_count=5, mount_retry_interval=10, 
            sleep_on_exit=10, submit_logs=None, docker_pull_timeout=None, docker_login_cmd="bash", docker_cmd=docker_cmd)
    
    # create test backend    
    from xtlib.cmd_core import CmdCore
    cmd_core = CmdCore(config, None, None)
    backend = cmd_core.create_backend(backend_name, compute_def)

    mount_helper = MountHelper(compute_def=compute_def, homebase=homebase, mountbase=mountbase, tmpbase=tmpbase, sudo_available=use_sudo, actions=actions, 
        use_username=True, use_allow_other=False, nonempty=True, backend=backend, config=config, args=args)

    scriptor = NodeScriptor(homebase=homebase, cwd="$HOME/.xt/cwd", controller_cmd=controller_cmd, 
        manual_docker=manual_docker, mount_helper=mount_helper, backend=backend, use_sudo=use_sudo, compute_def=compute_def, 
        default_docker_image=None, get_env_vars_from_file=False, config=config, args=args)
    
    fn_script, fn_inner = scriptor.generate_script()
    print("fn_script: {}".format(fn_script))
    print("fn_inner: {}".format(fn_inner))

if __name__ == "__main__":
    scriptor_test()