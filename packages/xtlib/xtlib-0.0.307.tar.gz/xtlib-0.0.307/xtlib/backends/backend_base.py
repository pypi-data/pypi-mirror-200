#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_base.py: provides a baseclass for backend classes, and defines the API they implement.
import os
import inspect
from time import time
from typing import List
from interface import implements

from xtlib.console import console

from xtlib import utils
from xtlib import errors
from xtlib import cs_utils
from xtlib import scriptor
from xtlib import pc_utils
from xtlib import run_errors
from xtlib import constants
from xtlib import file_utils
from xtlib import store_utils

from xtlib.backends.backend_interface import BackendInterface

class BackendBase(implements(BackendInterface)):

    '''
    Order of command building:
        - wrap_user_command() adds commands to cmds
        - add_mount_cmds
        - create_wrapper_and_inner() adds commands to docker_cmds
        - append_pre_docker_cmds()

    Order of command execution on node WITH docker:
        - pre_docker_cmds
        - docker_cmds
            - docker prep/install commands
            - docker pull with optional timeout
            - docker run (2-7 below)

    Order of command execution on node WITHOUT docker:
        1. pre_docker_cmds
        2. add_first_cmds
        3. add_setup_cmds
        4. add_other_cmds
        5. add_report_cmds
        6. mount cmds
        7. run controller (or direct run)
        8. node wrapup cmds
    '''
    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        self.compute = compute
        self.compute_def = compute_def
        self.blobfuse_index = 0
        self.fn_wrapped = None
        self.blobfuse_installed = False
        self.capture_setup_cmds = False
        self.echo_cmds = True
        self.default_docker_image = ""
        self.mounted_drives = []

        # TODO: change this to rely on API for this info
        self.add_time = config.get("logging", "add-timestamps")

        # if these are set to constant values, backend must use unique scripts for each node
        # default for backends is to pass these 3 args to their __wrapped__.xx script (philly is different)
        self.node_index = "$1"
        self.node_id = "node$1"
        self.run_name = "$2"
        self.mounting_enabled = True

        # if backend is running windows
        self.is_windows = False

        # if code should be generated for windows (if targeting a docker container, this can be different than self.is_windows)
        self.gen_for_windows = False
        
    # API
    def supports_setting_location(self):
        # not currently supported
        return False
    
    # API 
    def get_name(self):
        '''
        This method is called return the name of the backend service.
        '''
        pass

    # API 
    def build_node_script_and_adjust_runs(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, env_vars, args, cmds=None):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  At the
        time this is called, files can still be added to snapshot_dir.
        '''
        pass

    # API 
    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
            repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):
        raise Exception("backend API function not implemented: submit_job")

    # API 
    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):
        raise Exception("backend API function not implemented: view_status")

    # API 
    def get_client_cs(self, service_node_info):
        raise Exception("backend API function not implemented: get_client_cs")
    
    # API 
    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        '''
        return True

    # API 
    def cancel_runs_by_names(self, workspace, run_names, box_name):
        '''
        Args:
            workspace: the name of the workspace containing the run_names
            run_names: a list of run names
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of cancel_result records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs")

    # API 
    def cancel_runs_by_job(self, job_id, runs_by_box):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs_by_job")

    # API 
    def cancel_runs_by_user(self, ws_name, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs_by_user")

    # common code
    def append(self, cmds, cmd, expand=False, log=None, echo=None, add_time=None):

        if add_time is None:
            add_time = self.add_time

        if expand:
            cmd = self.expand_system_names(cmd)

        # if self.gen_for_windows and not cmd.startswith("@"):
        #     cmd = "@" + cmd

        if log and self.capture_setup_cmds:
            assert isinstance(log, str)
            
            if self.gen_for_windows:
                cmd = "{} > {}\\__{}__.log".format(cmd, constants.WINDOWS_AFTER_LOGS, log)
            else:
                cmd = "{} > {}/__{}__.log".format(cmd, constants.LINUX_AFTER_LOGS, log)

        if echo is None:
            echo = self.echo_cmds

        if echo:
            # avoid echo of super long (multiple line) commands
            max_echo_len = 300        
            cmd_text = cmd
            if len(cmd_text) > max_echo_len:
                cmd_text = cmd_text[0:max_echo_len-3] + "..."

            # ECHO the command before it is run 
            if self.gen_for_windows:
                # WINDOWS 
                cmd_text = cmd_text.replace(">", "^>")    # must escape the ">" to prevent cmd redirection

                if add_time:
                    # %date% is subject to local formatting, etc. so we use python instead
                    # cmd = '''python -c "import datetime as dt; print(dt.date.today().strftime('%m/%d/%Y'))"'''
                    # we use sed (.git install required) to remove double quotes here so that cmd piping can be echoed
                    #cmds.append('''echo "@%date% %time%     ++ {}" | sed 's/"//g' '''.format(cmd_text))
                    cmds.append('''echo "%date% %time%     ++ {}" | sed 's/^...../@/' '''.format(cmd_text))
                else:
                    cmds.append('''echo ++ {}'''.format(cmd_text))

            else:
                # LINUX 
                #cmd_text = cmd.replace(">", "\>")    # must escape the ">" to prevent cmd redirection
                cmd_text = "'{}'".format(cmd_text)

                if add_time:
                    cmds.append('''echo @$(date +%b-%d-%Y"  "%T)"     "++ {}'''.format(cmd_text))
                else:
                    cmds.append('''echo ++ {}'''.format(cmd_text))

        # finally, add the cmd to be run
        cmds.append(cmd)

    def get_activate_cmd(self, args):

        setup_name = args["setup"]
        setup_def = self.config.get_setup_from_target_def(self.compute_def, setup_name)
        activate_cmd = utils.safe_value(setup_def, "activate")

        if activate_cmd:
            if self.gen_for_windows:
                activate_cmd = activate_cmd.replace("$call ", "call ")
            else:
                activate_cmd = activate_cmd.replace("$call ", "")
                # Attempting to activate the Conda shell from within a bash script
                # fails, with Conda saying that the bash environment has not
                # been correctly initialized to use Conda.
                # This thread https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
                # eventually led me to the following command which is taken
                # from the lines of bash script that Conda appends to your
                # .bashrc file upon installation. This command is what
                # allows you to activate the Conda environment within a
                # bash shell. It returns a script generated by Conda
                # which is executed, and which stes up the conda
                # activate / deactivate commands in the encironment.
                conda_shell_bash_hook_cmd = 'eval "$(conda shell.bash hook)"'
                activate_cmd = "{} && {}".format(
                    conda_shell_bash_hook_cmd, activate_cmd)

        return activate_cmd

    def get_service_name(self):
        if not "service" in self.compute_def:
            errors.config_error("missing 'service' property for xt config file compute target '{}'".format(self.compute))
        service_name = self.compute_def["service"]
        return service_name

    def object_to_dict(self, obj, columns):
       obj_dict = {col: getattr(obj, col) for col in columns if hasattr(obj, col)}
       return obj_dict
        
    # def append_install_blobfuse_cmds(self, cmds, sudo_available):
    #     # only install it once per backend instance

    #     if not self.blobfuse_installed:
    #         self.append_title(cmds, "INSTALL BLOBFUSE:")
    #         sudo = "sudo " if sudo_available else ""

    #         # configure apt for microsoft products
    #         self.append(cmds, "{}wget https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb".format(sudo), log="wget")
    #         self.append(cmds, "{}dpkg -i packages-microsoft-prod.deb".format(sudo), log="dpkg")
            
    #         self.append(cmds, "{}apt-get -y update".format(sudo), log="apt_update")

    #         # install blobfuse
    #         # without specifying version, we get version 1.2.3 on AML which breaks our code
    #         version = "1.0.3"         
    #         self.append(cmds, "{}apt-get -y install blobfuse={}".format(sudo, version), log="apt_install_blobfuse")

    #         # #self.append(cmds, "{}modprobe fuse".format(sudo))
    #         # self.append(cmds, "apt-get -y install modprobe")
    #         # self.append(cmds, "modprobe fuse")

    #         self.blobfuse_installed = True

    # def create_blobfuse_commands(self, storage_name, storage_key, sudo_available, mount_requests, install_blobfuse, 
    #         use_username=True, use_allow_other=True, nonempty=False, tmpbase="$HOME", args=None):
    #     username = "$USER"
    #     cmds = []
    #     sudo = "sudo " if sudo_available else ""
    #     mount_retry_count = args["mount_retry_count"]
    #     mount_retry_interval = args["mount_retry_interval"]

    #     # for each mount request
    #     for md in mount_requests:
    #         mnt_dir = md["mnt_dir"]
    #         container_name = md["container"]
    #         readonly = md["readonly"]

    #         self.blobfuse_index += 1
    #         #console.print("tmpbase=", tmpbase)

    #         #tmp_dir = "/mnt/resource/blobfusetmp{}".format(self.blobfuse_index)
    #         tmp_dir = tmpbase + "/blobfusetmp{}".format(self.blobfuse_index)
    #         fn_config = tmpbase + "/fuse{}.cfg".format(self.blobfuse_index)
    #         readonly_opt = "-o ro" if readonly else ""
    #         nonempty_opt = "-o nonempty" if nonempty else ""

    #         self.mounted_drives.append(mnt_dir)

    #         self.append(cmds, "{}mkdir {} -p".format(sudo, mnt_dir))

    #         if use_username:
    #             self.append(cmds, "{}chown {} {}".format(sudo, username, mnt_dir))

    #         allow_other = "-o allow_other" if use_allow_other else ""

    #         # create temp dir (required by blobfuse)
    #         self.append(cmds, "mkdir -p {}".format(tmp_dir))

    #         # create fuse config file (clunky but it works)
    #         self.append(cmds, "echo accountName {} > {}".format(storage_name, fn_config))
    #         self.append(cmds, "echo accountKey {} >> {}".format(storage_key, fn_config))
    #         self.append(cmds, "echo containerName {} >> {}".format(container_name, fn_config))

    #         #"echo here is the config file '{}' contents".format(fn_config),
    #         #"more {}".format(fn_config),

    #         # keep it private 
    #         self.append(cmds, "chmod 600 {}".format(fn_config))
    #         self.append(cmds, "blobfuse -v")

    #         # need to wrap this command with retry logic (similiar to docker run)
    #         #     pull_cmd = '''timeout {} bash -c "until {}; do '''.format(timeout, constants.FN_DOCKER_PULL_SH) + \
    #         #         '''echo XT: docker pull failed.  retrying...; sleep 60; done" '''

    #         blobfuse_cmd = "{}blobfuse {} --tmp-path={}  --config-file={} {} -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 {} {}" \
    #             .format(sudo, mnt_dir, tmp_dir, fn_config, readonly_opt, allow_other, nonempty_opt)

    #         if mount_retry_count:
    #             # retry the blobfuse command as per count/interval
    #             range = "{1.." + str(mount_retry_count) + "}"
    #             retry_cmd = "for i in {}; do {} && break || echo error in blobfuse mount: sleeping... ; sleep {}; echo retrying blobfuse mount...; done".format(range, blobfuse_cmd, mount_retry_interval)
    #             self.append(cmds, retry_cmd)

    #         else:       
    #             # normal blobfuse cmd (no retries)     
    #             self.append(cmds, blobfuse_cmd)

    #         #self.append(cmds, "echo just ran blobfuse, here is ls -l on mnt_dir", echo=False)
    #         self.append_dir(cmds, mnt_dir)

    #     return cmds

    # def create_download_commands(self, xt_path, create_dest_dirs, sudo_available, download_requests, 
    #         for_windows=False, use_username=True):
    #     '''
    #     Lessons learned here:
    #         - we want to create MNT root and subdirectories all without SUDO (so we don't create access for download process 
    #           or subsequent reading by normal user)
              
    #         - previously, we were created the MNT folder indirectly thru our blobfuse mounting code, where we create the mapping folder
    #           with SUDO.  This created a problem later when we create the download directory, it becomes created with ROOT and then normal
    #           user code cannot copy to that folder.
    #     '''
    #     cmds = []
    #     #username = "$USER"
    #     #sudo = "sudo " if (sudo_available and not for_windows) else ""
    #     #sudo = "sudo " if (sudo_available and not for_windows) else ""

    #     # for each mount request
    #     for md in download_requests:
    #         container_name = md["container"]
    #         blob_path = md["blob_path"]
    #         dest_dir = md["dest_dir"]

    #         if create_dest_dirs:
    #             if for_windows:
    #                 # fix slashes for windows
    #                 dest_dir = dest_dir.replace("/", "\\")
    #                 sub_cmds = \
    #                 [ 
    #                     "mkdir {} ".format(dest_dir),
    #                 ]
    #             else:
    #                 sub_cmds = \
    #                 [ 
    #                     # don't use SUDO here; we need dir accessible by current user
    #                     "mkdir -p {}".format(dest_dir),
    #                 ]
    #                 # if use_username:
    #                 #     sub_cmds.append("{}chown {} {}".format(sudo, username, dest_dir))

    #             for sc in sub_cmds:
    #                 self.append(cmds, sc)

    #         # # remove old directory from previous run (singularity doesn't clean these up?)
    #         # mc = "{}rm -rf {} ".format(sudo, dest_dir)
    #         # self.append(cmds, mc)

    #         cmd = "{} download /{}/{} {}".format(xt_path, container_name, blob_path, dest_dir)
    #         self.append(cmds, cmd, expand=True, log="download")

    #         self.append_dir(cmds, dest_dir)

    #     return cmds        

    # def emit_mount_cmds(self, cmds, storage_name, storage_key, container, mnt_path, is_writable, 
    #     install_blobfuse, sudo_available, use_username, use_allow_other, 
    #     nonempty=False, cleanup_needed=False, tmpbase="$HOME", args=None):

    #     # NOTE: OK to use SUDO here (for blobfuse dirs)

    #     if self.mounting_enabled:
    #         user_install_blobfuse = args["install_blobfuse"]
    #         if install_blobfuse and user_install_blobfuse:
    #             self.append_install_blobfuse_cmds(cmds, sudo_available)

    #         if self.gen_for_windows:
    #             # TODO: provide pseudo-mount for local machine by using data-local and store-local config properties
    #             errors.combo_error("Mounting of Azure storage (for '{}') not supported by target OS (Windows)".\
    #                 format(storage_name))

    #         if cleanup_needed:
    #             # on pool machines, for any action, always UNMOUNT mnt_dir 
    #             # also, always zap the folder in case in was used in downloading files
    #             sudo = "sudo " if sudo_available else ""

    #             # only do an unmount if dir exists
    #             self.append(cmds,"ls {} 2>/dev/null && {}fusermount -u -q {}".format(mnt_path, sudo, mnt_path))

    #             # do NOT call rm as it can delete cloud data if fusermount -u failed 
    #             #self.append(cmds,"{}rm -rf {}".format(sudo, mnt_path))

    #         requests = [ {"container": container, "mnt_dir": mnt_path, "readonly": not is_writable} ]
    #         sub_cmds = self.create_blobfuse_commands(storage_name, storage_key, sudo_available, requests, install_blobfuse=install_blobfuse,
    #             use_username=use_username, use_allow_other=use_allow_other, nonempty=nonempty, tmpbase=tmpbase, args=args)
    #         cmds += sub_cmds

    # def process_action(self, cmds, action, mnt_path, container, store_data_dir, env_var_name, is_writable,
    #     storage_name, storage_key, sudo_available=True, cleanup_needed=False, is_windows=False, use_username=True, 
    #     install_blobfuse=False, use_allow_other=True, nonempty=False, tmpbase=None, args=None):

    #     gen_for_windows = self.set_gen_for_windows(is_windows, args)

    #     if action == "mount":
    #         self.emit_mount_cmds(cmds, storage_name, storage_key, container, mnt_path=mnt_path, 
    #             is_writable=is_writable, install_blobfuse=install_blobfuse, sudo_available=sudo_available, 
    #             use_username=use_username, use_allow_other=use_allow_other, 
    #             nonempty=nonempty, cleanup_needed=cleanup_needed, tmpbase=tmpbase, args=args)

    #         self.append_export(cmds, env_var_name, "{}/{}".format(mnt_path, store_data_dir))


    #     elif action == "use_local":
    #         self.append(cmds, "echo USING LOCAL path for ENV[{}]".format(env_var_name), echo=False)
    #         self.append_export(cmds, env_var_name, store_data_dir, value_is_windows=self.gen_for_windows)

    #     elif action == "download":

    #         # keep all DOWNLOAD directories owned by normal user (not ROOT)
    #         sudo_available = False

    #         # here, commands must be obey gen_for_windows
    #         self.append(cmds, "echo DOWNLOADING {} from container {}".format(mnt_path, container))

    #         if gen_for_windows:
    #             self.append_export(cmds, env_var_name, store_data_dir, value_is_windows=True)
    #             self.append(cmds, "echo setting {}={}".format(env_var_name, store_data_dir, value_is_windows=True))
    #         else:
    #             full_mnt_path =  mnt_path + "/" + store_data_dir
    #             self.append_export(cmds, env_var_name, full_mnt_path, value_is_windows=False)
    #             self.append(cmds, "echo setting {}={}".format(env_var_name, full_mnt_path, value_is_windows=False))

    #         # make it look like this is parent dir
    #         dest_dir_ext = mnt_path + "/" + store_data_dir

    #         requests = [ {"container": container, "blob_path": store_data_dir, "dest_dir": dest_dir_ext} ]
    #         sub_cmds = self.create_download_commands("xt", True, sudo_available, requests, for_windows=gen_for_windows, 
    #             use_username=use_username)
    #         cmds += sub_cmds

    # def get_action_args(self, args):
    #     store_data_dir = args["data_share_path"]
    #     data_action = args["data_action"]
    #     data_writable = args["data_writable"]

    #     store_model_dir = args["model_share_path"]
    #     model_action = args["model_action"]
    #     model_writable = args["model_writable"]

    #     storage_name = args["storage"]
    #     storage_info = self.config.get("external-services", storage_name, default_value=None)
    #     if not storage_info:
    #         self.config_error("storage name '{}' not defined in [external-services] in config file".format(storage_name))

    #     # TODO: remove this reliance on specific storage providers 
    #     storage_key = storage_info["key"] if "key" in storage_info else None

    #     return store_data_dir, data_action, data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key

    # def append_python_path(self, cmds):
    #     if self.gen_for_windows:
    #         self.add_info(cmds, "PYTHONPATH", "%PYTHONPATH%")
    #     else:
    #        self.add_info(cmds, "PYTHONPATH", "$PYTHONPATH")

    # def append_export(self, cmds, name, value, value_is_windows=False, fix_value=True):
    #     '''
    #     args:
    #         - cmds: the set of commands to append the export cmd to
    #         - name: the name of the environment var to set/export
    #         - value: the string value (could have $xx or %xx% variables in a list)
    #         - value_is_windows: if value is windows style (vs. linux style)
    #     '''
    #     # ensure value is a str
    #     value = str(value)

    #     if self.gen_for_windows:

    #         if fix_value and not value_is_windows:
    #             value = value.replace("$HOME", "%USERPROFILE%")
    #             # need to split value into parts to surround them with "%"
    #             parts = value.split(":")
    #             for i, part in enumerate(parts):
    #                 if part == "$HOME":
    #                     parts[i] = "%USERPROFILE%"
    #                 elif part.startswith("$"):
    #                     parts[i] = "%" + part[1:] + "%"
    #             value = ";".join(parts)
    #         cmd = "set {}={}".format(name, value)

    #     else:
    #         if fix_value and value_is_windows:
    #             # need to split value into parts to remove surrounding %
    #             parts = value.split(";")
    #             for i, part in enumerate(parts):
    #                 if part.startswith("%") and part.endswith("%"):
    #                     parts[i] = "$" + part[1:-1] 
    #             value = ":".join(parts)
                    
    #         cmd = "export {}={}".format(name, value)

    #     self.append(cmds, cmd)

    def expand_system_names(self, cmd):
        if self.gen_for_windows:
            cmd = cmd.replace("$call", "call")
            cmd = cmd.replace("$export", "set")
        else:
            cmd = cmd.replace("$call ", "")
            cmd = cmd.replace("$export", "export")

        if "$current_conda_env" in cmd:
            conda = pc_utils.get_conda_env() 
            if conda:
                cmd = cmd.replace("$current_conda_env", conda)
        
        return cmd

    # def add_first_cmds(self, cmds, homebase, cwd, args, copy_code=False):

    #     # don't add this as a cmd (breaks our script on philly)
    #     # if not self.gen_for_windows:
    #     #     self.append(cmds, "#!/bin/sh")

    #     report_text = "after docker reports" if args["docker_cmd"] else "reports"
    #     self.add_reports(cmds, report_text, args)

    #     self.append_title(cmds, "FIRST CMDS:")

    #     self.export_now_to_var(cmds, "XT_PREP_START_TIME")

    #     # remember original dir for service log files at end
    #     pwd_cmd = "%CD%" if self.gen_for_windows else "$(pwd)"
    #     self.append_export(cmds, "XT_ORIG_WORKDIR", pwd_cmd, fix_value=False)

    #     if homebase == ".":
    #         self.append_export(cmds, "XT_HOMEBASE", pwd_cmd, fix_value=False)
    #     else:
    #         self.append_export(cmds, "XT_HOMEBASE", homebase, fix_value=False)

    #     if cwd == ".":
    #         value = "%CD%" if self.gen_for_windows else "$(pwd)"
    #         cwd = value
    #         self.append_export(cmds, "XT_CWD", value, fix_value=False)
    #     else:
    #         self.append_export(cmds, "XT_CWD", cwd, fix_value=False)

    #     self.append_export(cmds, "XT_NODE_ID", self.node_id)
    #     self.append_export(cmds, "XT_RUN_NAME", self.run_name)
    #     self.append_export(cmds, "XT_MOUNTING_ENABLED", self.mounting_enabled)

    #     job_id = args["job_id"]
    #     ws_name = args["workspace"]
    #     self.append_export(cmds, "XT_JOB_ID", job_id)
    #     self.append_export(cmds, "XT_WORKSPACE_NAME", ws_name)

    #     # for debugging version 1 vs. 2 issues
    #     self.append_export(cmds, "XT_STORE_NAME", self.config.get("store"))
    #     self.append_export(cmds, "XT_JOBS_CONTAINER_NAME", store_utils.get_jobs_container(args["workspace"]))
    #     self.append_export(cmds, "XT_STORAGE_FORMAT", store_utils.STORAGE_FORMAT)

    #     # workaround for Pytorch 1.5/1.6 issue
    #     # note: this is set in the std xtlib docker files but something in AML must be changing it
    #     # so we reset it to GNU here (to avoid MKL NOT COMPATIBLE error in AML runs)
    #     self.append(cmds, "echo before setting mkl is $MKL_THREADING_LAYER", echo=False)
    #     self.append_export(cmds, "MKL_THREADING_LAYER", "GNU")

    #     self.add_info_cmds(cmds, args)

    #     # debug
    #     self.append_dir(cmds)

    #     if cwd != ".":
    #         #cwd = homebase
    #         cwd = file_utils.fix_slashes(cwd, is_linux=not self.gen_for_windows, protect_ws_run_name=False)

    #         if copy_code:
    #             self.append_title(cmds, "COPY/UNZIP CODE TO CWD:")
    #         else:
    #             self.append_title(cmds, "CHANGE TO CONTROLLER DIR:")

    #         if self.gen_for_windows:
    #             self.append(cmds, "mkdir {} 2>nul".format(cwd))
    #         else:
    #             self.append(cmds, "mkdir -p {}".format(cwd))

    #         if copy_code:
    #             self.append(cmds, "cp __* {}".format(cwd))
    #             # self.append(cmds, "cp -r code {}".format(cwd))
    #             # self.append(cmds, "cp -r xtlib {}".format(cwd))

    #             # unzip code
    #             self.append_unzip(cmds, "xt_code.zip", cwd, echo=True)

    #         self.append(cmds, "cd {}".format(cwd))
    #         self.append(cmds, 'echo current dir: {}'.format("%cd%" if self.gen_for_windows else "$PWD"), echo=False)

    #         self.append_dir(cmds, ".")

    #     # ensure we have dir for logs
    #     if self.gen_for_windows:
    #         self.append(cmds, "md {}".format(constants.WINDOWS_AFTER_LOGS))
    #     else:
    #         self.append(cmds, "mkdir -p {}".format(constants.LINUX_AFTER_LOGS))

    # def add_info(self, cmds, title, linux_cmd, windows_cmd=None):

    #     # expand all titles to same size for uniform columns
    #     title = (title + ":").ljust(15)

    #     if self.gen_for_windows:
    #         windows_cmd = windows_cmd or linux_cmd
    #         cmd = '''echo {} {}'''.format(title, windows_cmd)
    #     else:
    #         # these embedded double quotes enable the tab char to be recognized on linux
    #         cmd = '''echo "{} {}"'''.format(title, linux_cmd)

    #     self.append(cmds, cmd, echo=False)

    # def append_dir(self, cmds, path=".", recursive=False):
    #     # limit to 30 lines

    #     display_path = path
    #     if path == ".":
    #         display_path = "%CD%" if self.gen_for_windows else "$PWD"

    #     self.append_title(cmds, "DIR: " + display_path)

    #     if False:  #self.gen_for_windows:
    #         cmd = "dir {} | head -n 30".format(path)
    #     else:
    #         # grep is used to supress the distracting "total" line
    #         # head is used to limit to 30 lines
    #         opts = "-R " if recursive else ""
    #         #cmd = "ls -lt {}{} | grep -vh '^total' | head -n 30".format(opts, path)
    #         cmd = "ls -l {}{} | grep -vh '^total'".format(opts, path)

    #     self.append(cmds, cmd, echo=True)

    # def append_unzip(self, cmds, fn_zip, dest_dir, echo=True):
    #     self.append(cmds, '''python -c "import zipfile; zipfile.ZipFile('{}').extractall('{}')"'''. \
    #         format(fn_zip, dest_dir), echo=echo)

    # def append_title(self, cmds, title, echo=True, double=False, index=None):
    #     if double:
    #         line = "echo =========================================="
    #     else:
    #         line = "echo ------------------------------------------"

    #     self.echo_cmds = False
    #     title_plus = "'{} ('$(date +%b-%d-%Y\", @\"%T)')'".format(title)

    #     if index is not None:
    #         cmds.insert(index, line)
    #         cmds.insert(index, "echo " + title_plus)
    #         cmds.insert(index, line)
    #     else:
    #         cmds.append(line)
    #         cmds.append("echo " + title_plus)
    #         cmds.append(line)

    #     self.echo_cmds = echo

    # def add_info_cmds(self, cmds, args):
    #     self.append_title(cmds, "BEFORE environment:", echo=False)

    #     target = args["target"]
    #     docker_name = args["docker"]
    #     docker_image, login_server, docker_registry, _ = self.config.get_docker_info(target, docker_name, required=False)
    #     docker_image = login_server + "/" + docker_image if login_server else docker_image

    #     if not docker_image:
    #         docker_image = self.default_docker_image

    #     job_id = args["job_id"]
    #     node_info = self.config.get_target_desc(target, self)
    #     node_info = node_info.replace("target=", "")

    #     self.add_info(cmds, "job id", job_id)
    #     self.add_info(cmds, "node id", self.node_id)
    #     self.add_info(cmds, "run name", self.run_name)
    #     self.add_info(cmds, "target", node_info)
    #     self.add_info(cmds, "hostname", "$(hostname)", "%COMPUTERNAME%")

    #     if self.gen_for_windows:
    #         # windows 
    #         cmds.append("ipconfig | findstr IPv4 > __t__ && set /p xt_tmp= < __t__")
    #         cmds.append("set xt_tmp=%xt_tmp:~40,99%")     # extract string starting at offset 40
    #         self.add_info(cmds, "IP address", "%xt_tmp%")
    #         cmds.append("ver | findstr Mic > __t__ && set /p xt_tmp= < __t__")
    #         self.add_info(cmds, "OS version", "%xt_tmp%")
    #         self.add_info(cmds, "Conda env", "$CONDA_DEFAULT_ENV", "%CONDA_DEFAULT_ENV%")
    #         self.add_info(cmds, "In docker", "$IN_DOCKER", "False")
    #         self.add_info(cmds, "Image request", docker_image)
    #         self.add_info(cmds, "Image name", "$DOCKER_IMAGE_NAME", "%DOCKER_IMAGE_NAME%")
    #         cmds.append("wmic path win32_VideoController get name | findstr -V Name | head -n 1 > __t__ && set /p xt_tmp= < __t__")
    #         self.add_info(cmds, "GPU type", "%xt_tmp%")
    #     else:
    #         # linux
    #         self.add_info(cmds, "IP address", "$(hostname -I | awk '{print $2}')")
    #         self.add_info(cmds, "OS version", '''$(cat /etc/os-release | grep PRETTY_NAME | cut -d '"' -f2)''')
    #         self.add_info(cmds, "Conda env", "$CONDA_DEFAULT_ENV", "%CONDA_DEFAULT_ENV%")
    #         self.append(cmds, "if [ -f /.dockerenv ]; then export IN_DOCKER=True; else export IN_DOCKER=False; fi")
    #         self.add_info(cmds, "In docker", "$IN_DOCKER", "False")
    #         self.add_info(cmds, "Image request", docker_image)
    #         self.add_info(cmds, "Image name", "$DOCKER_IMAGE_NAME", "%DOCKER_IMAGE_NAME%")
    #         self.add_info(cmds, "GPU type", "$(nvidia-smi -L | cut -d'(' -f1)")

    #     self.add_python_info(cmds)

    #     # debug
    #     #self.append(cmds, "which python")
    #     #self.append(cmds, "pip show torch")

    #     # TORCH version (before pip install)
    #     target_cmd = '''python -c "import torch; print('PyTorch:'.ljust(15) + ' ' + torch.__version__ + ', CUDA available: ' + str(torch.cuda.is_available()))"'''
    #     self.append_package_test(cmds, "torch", target_cmd, "PyTorch")

    #     self.add_info(cmds, "running", "$(basename $0)", "%0")
    #     self.add_info(cmds, "current dir", "$(pwd)", "%CD%")
    #     self.add_info(cmds, "username", "$(whoami)", "%USERNAME%")

    # def append_package_test(self, cmds, package_to_import, target_cmd, ni_name):
    #     nul_name = "nul" if self.gen_for_windows else "/dev/null"

    #     cond_cmd = '''python -c "import {}" 2>{}'''.format(package_to_import, nul_name)

    #     if self.gen_for_windows:
    #         else_cmd = "echo {}: \tnot installed".format(ni_name)
    #     else:
    #         # need to surround with double quotes for tab to be recognized
    #         else_cmd = 'echo "{}: \tnot installed"'.format(ni_name)

    #     cmd = "{} && {} 2>{}".format(cond_cmd, target_cmd, nul_name)
    #     cmd2 = "{} || {}".format(cond_cmd, else_cmd)
    #     self.append(cmds, cmd)
    #     self.append(cmds, cmd2)

    # def add_report_cmds(self, cmds, include_pytorch=True, args=None):

    #     self.framework_report(cmds)
    #     self.xt_report(cmds)

    # def add_python_info(self, cmds):
    #     # the "2>&1" is used to join stderr to stdout here (since versions of python use both)
    #     if self.gen_for_windows:
    #         cmds.append("python -V > __t__ 2>&1 && set /p xt_tmp= < __t__")
    #         self.add_info(cmds, "Python", "%xt_tmp%")
    #     else:
    #         # cmds.append("python -V > __t__ 2>&1 && xt_tmp=$(cat  __t__)")
    #         # self.add_info(cmds, "Python", "$xt_tmp")
    #         self.add_info(cmds, "Python", "$(python -V 2>&1)")

    # def framework_report(self, cmds):
    #     self.append_title(cmds, "FRAMEWORK report:", False)

    #     self.add_python_info(cmds)

    #     self.add_info(cmds, "Conda env", "$CONDA_DEFAULT_ENV", "%CONDA_DEFAULT_ENV%")
        
    #     # PYTORCH
    #     target_cmd = '''python -c "import torch; print('PyTorch:'.ljust(15) + ' ' + torch.__version__ + ', CUDA available: ' + str(torch.cuda.is_available()))"'''
    #     self.append_package_test(cmds, "torch", target_cmd, "PyTorch")

    #     # CUDA
    #     target_cmd = '''python -c "import torch; print('cuda version:'.ljust(15) + ' ' + torch.version.cuda)"'''
    #     self.append_package_test(cmds, "torch", target_cmd, "cuda")

    #     # TORCHVISION
    #     target_cmd = '''python -c "import torchvision; print('torchvision:'.ljust(15) + ' ' + torchvision.__version__ )"'''
    #     self.append_package_test(cmds, "torchvision", target_cmd, "torchvision")

    #     # for now, OMIT tensorflow (can take 30-60 secs to initialize cuda, etc.)
    #     # # TENSORFLOW
    #     # target_cmd = '''python -c "import tensorflow as tf; print('Tensorflow:'.ljust(15) + ' ' + tf.__version__ + ', CUDA available: ' + str(tf.test.is_gpu_available()))"'''
    #     # self.append_package_test(cmds, "tensorflow", target_cmd, "Tensorflow")

    def xt_report(self, cmds):

        self.append_title(cmds, "XT report:", True)
        if self.gen_for_windows:
            self.append(cmds, "which xt python conda")
        else:
            self.append(cmds, "which xt python conda blobfuse")

        self.append(cmds, "xt --version", echo=True)

    def add_other_cmds(self, cmds, args):
        pp = args["other_cmds"]

        if pp:
            #console.print("other_cmds: {}".format(pp))
            self.append_title(cmds, "OTHER setup cmds:", False)
            for cmd in pp:
                self.append(cmds, cmd)

            self.cd_back_to_setup_dir(cmds)

    def set_gen_for_windows(self, for_windows: bool, args: List[str]):
        docker_cmd = args["docker_cmd"]
        docker_is_windows = args["docker_is_windows"]

        if docker_cmd:
            gen_for_windows = docker_is_windows
        else:
            gen_for_windows = self.is_windows

        self.gen_for_windows = gen_for_windows
        return gen_for_windows

    # def wrap_user_command(self, user_parts, snapshot_dir, store_data_dir, data_action, data_writable, \
    #     store_model_dir, model_action, model_writable, storage_name, storage_key, actions, is_windows, 
    #     sudo_available=True, username=None, use_username=True, install_blobfuse=False, pre_setup_cmds=None,
    #     setup=None, post_setup_cmds=None, args=None, nonempty=False, use_allow_other=True, 
    #     remove_zip=True, node_index="$1", run_name="$2", homebase="$HOME", cwd="$HOME/.xt/cwd", 
    #     copy_code=False, mountbase=None, tmpbase=None):
    #     '''
    #     we need to run several commands to configure the target machine for our run, and then run the user's commands (user_parts).
    #     we do this by writing all the commands (config cmds and user_parts) to shell script or batch file that resides in the 
    #     "snapsnot_dir".  all files in the snapshot_dir will be zipped and uploaded to the job store at job submit time, and then
    #     downloaded and unzipped on the target machine at run launch time.

    #     "homebase" is the base directory used to build:
    #         - controller working dir   (homebase/.xt/cwd)
    #         - mounting paths (homebase/.xt/mnt/xxx)
    #         - local data paths (homebase/.xt.local/xxx)

    #     '''
    #     self.node_index = node_index
    #     self.node_id = "node" + str(node_index)
    #     self.run_name = run_name

    #     gen_for_windows = self.set_gen_for_windows(is_windows, args)
    #     self.capture_setup_cmds = args["capture_setup_cmds"]

    #     if gen_for_windows:
    #         self.mounting_enabled = False

    #     docker_cmd = args["docker_cmd"]
    #     cmds = []

    #     if gen_for_windows:
    #         cmds.append("@echo off")

    #     if pre_setup_cmds:
    #         cmds += pre_setup_cmds

    #     self.add_first_cmds(cmds, homebase, cwd, args=args, copy_code=copy_code)

    #     if self.get_service_name() == "pool" and docker_cmd:
    #         # for pool jobs running under docker, copy source code into docker CWD 
    #         # to isolate effect of docker jobs to docker container & to avoid ROOT vs. user file issues

    #         self.append(cmds, 'cp -r /usr/src/. .', echo=True)

    #     # TODO: don't call setup_cmds for AML backend (it seems to cover conda/pip packages in its image build)
    #     self.add_setup_cmds(cmds, remove_zip, gen_for_windows=gen_for_windows, args=args)

    #     self.add_other_cmds(cmds, args)

    #     if username:
    #         self.append(cmds, "$export USER=" + username, expand=True)

    #     if not mountbase:
    #         mountbase = homebase

    #     if not tmpbase:
    #         tmpbase = homebase

    #     self.add_mount_cmds(cmds, sudo_available, storage_name, storage_key, 
    #         actions, data_action, model_action, store_data_dir, store_model_dir, data_writable, model_writable,
    #         install_blobfuse=install_blobfuse, use_username=use_username, 
    #         use_allow_other=use_allow_other, nonempty=nonempty, homebase=homebase, mountbase=mountbase, 
    #         tmpbase=tmpbase, args=args)

    #     # add post setup commands now
    #     if post_setup_cmds:
    #         cmds += post_setup_cmds

    #     # run controller or user's cmd
    #     user_cmd = " ".join(user_parts)
    #     fn_wrapped = self.create_wrapper_and_inner(cmds, user_cmd, sudo_available, args)

    #     return fn_wrapped

    # def fix_path(self, path):
    #     if self.gen_for_windows:
    #         path = path.replace("$HOME", "%USERPROFILE%")
    #         path = path.replace("/", "\\")

    #     return path

    # def add_mount_cmds(self, cmds, sudo_available, storage_name, storage_key, 
    #     actions, data_action, model_action, store_data_dir, store_model_dir, data_writable=True, model_writable=False, 
    #     use_username=None, use_allow_other=None, nonempty=False, install_blobfuse=True, homebase="$HOME",
    #     mountbase="$HOME", tmpbase="$HOME", args=None):

    #     gen_for_windows = self.gen_for_windows
    #     workspace = args["workspace"]
    #     job_id = args["job_id"]

    #     # create the MNT base folder WITHOUT SUDO
    #     # this is required for accessing data/models as normal user
    #     self.append(cmds, "mkdir -p {}/.xt/mnt".format(mountbase))

    #     # put mnt paths in user's home dir so sudo isn't needed to create/mount
    #     if self.mounting_enabled:
    #         jobs_mount_dir = mountbase + "/.xt/mnt/jobs_container"
    #         workspace_mount_dir = mountbase + "/.xt/mnt/workspace_container"
    #         data_mount_dir = mountbase + "/.xt/mnt/data_container"
    #         model_mount_dir = mountbase + "/.xt/mnt/models_container"
    #     else:
    #         if self.gen_for_windows:
    #             jobs_mount_dir = mountbase + "\\.xt\\local\\jobs_container"
    #             workspace_mount_dir = mountbase + "\\.xt\\local\\workspace_container"
    #             data_mount_dir = mountbase + "\\.xt\\local\\data_container"
    #             model_mount_dir = mountbase + "\\.xt\\local\\models_container"
    #         else:
    #             jobs_mount_dir = mountbase + "/.xt/local/jobs_container"
    #             workspace_mount_dir = mountbase + "/.xt/local/workspace_container"
    #             data_mount_dir = mountbase + "/.xt/local/data_container"
    #             model_mount_dir = mountbase + "/.xt/local/models_container"

    #     # emit cmds to MOUNT WORKSPACE and export/set releated environment variables
    #     if not gen_for_windows:
    #         # on linux, always mount WORKSPACE container
    #         workspace = args["workspace"]

    #         if self.mounting_enabled:
    #             user_install_blobfuse = args["install_blobfuse"]
    #             if install_blobfuse and user_install_blobfuse:
    #                 self.append_install_blobfuse_cmds(cmds, sudo_available)

    #             # mount workspace to /mnt/xt_workspace
    #             self.append_title(cmds, "MOUNT WORKSPACE container to path:")
    #             self.emit_mount_cmds(cmds, storage_name, storage_key, container=workspace, 
    #                 mnt_path=workspace_mount_dir, is_writable=True, install_blobfuse=False, 
    #                 sudo_available=sudo_available, use_username=use_username, use_allow_other=use_allow_other, 
    #                 nonempty=nonempty, cleanup_needed=True, tmpbase=tmpbase, args=args)

    #         # on linux, always mount JOBS container
    #         jobs_container = store_utils.get_jobs_container(workspace)

    #         if self.mounting_enabled:

    #             # mount workspace to /mnt/xt_workspace
    #             self.append_title(cmds, "MOUNT JOBS container to path:")
    #             self.emit_mount_cmds(cmds, storage_name, storage_key, container=jobs_container, 
    #                 mnt_path=jobs_mount_dir, is_writable=True, install_blobfuse=False, 
    #                 sudo_available=sudo_available, use_username=use_username, use_allow_other=use_allow_other, 
    #                 nonempty=nonempty, cleanup_needed=True, tmpbase=tmpbase, args=args)

    #         self.append_title(cmds, "EXPORT related environment variables:")

    #     # on windows or linux, always define XT_OUTPUT_DIR  (even if it is not mounted)
    #     # XT_OUTPUT_DIR
    #     run_path = store_utils.get_run_path(job_id, self.run_name) 
    #     store_path = "{}/{}/output".format(workspace_mount_dir, run_path)
    #     self.define_xt_dir(cmds, "XT_OUTPUT_DIR", store_path)

    #     # on windows or linux, always define XT_NODE_DIR  (even if it is not mounted)
    #     # XT_NODE_DIR
    #     store_path = "{}/jobs/{}/nodes/node{}".format(jobs_mount_dir, job_id, self.node_index)
    #     self.define_xt_dir(cmds, "XT_NODE_DIR", store_path)

    #     # emit cmds to MOUNT or DOWNLOAD data
    #     if "data" in actions and data_action != "none":
    #         self.append_title(cmds, "MOUNT/DOWNLOAD DATA:")
    #         self.process_action(cmds, data_action, data_mount_dir, store_utils.DATA_STORE_ROOT, store_data_dir, "XT_DATA_DIR",
    #             data_writable, storage_name, storage_key, sudo_available=sudo_available, cleanup_needed=True, 
    #             is_windows=gen_for_windows, use_username=use_username, install_blobfuse=False, nonempty=nonempty,
    #             use_allow_other=use_allow_other, tmpbase=tmpbase, args=args)

    #     # emit cmds to MOUNT or DOWNLOAD model
    #     if "model" in actions and model_action != "none":
    #         self.append_title(cmds, "MOUNT/DOWNLOAD MODELS:")
    #         self.process_action(cmds, model_action, model_mount_dir, store_utils.MODELS_STORE_ROOT, store_model_dir, "XT_MODEL_DIR",
    #             model_writable, storage_name, storage_key, sudo_available=sudo_available, cleanup_needed=True, 
    #             is_windows=gen_for_windows, use_username=use_username, install_blobfuse=False, nonempty=nonempty,
    #             use_allow_other=use_allow_other, tmpbase=tmpbase, args=args)

    def define_xt_dir(self, cmds, name, path):

        # ensure dir is empty but present
        if self.gen_for_windows:
            path = file_utils.fix_slashes(path, False, protect_ws_run_name=False)
            self.append_export(cmds, name, path, fix_value=False)
            self.append(cmds, "rd /s /q {}".format(path))
            self.append(cmds, 'mkdir "{}"'.format(path))
        else:
            path = file_utils.fix_slashes(path, True, protect_ws_run_name=False)
            self.append_export(cmds, name, path)
            self.append(cmds, "rm -rf {}".format(path))
            self.append(cmds, 'mkdir -p "{}"'.format(path))

        self.append_dir(cmds, path)

    # def add_log_upload_cmds(self, cmds, args):
    #     '''
    #     We try to not rely on xtlib being installed in the wrapper script so that
    #     the user can access and view logs about problems he may have installing 
    #     xtlib.  
        
    #     The one exception we make is the local Windows machine, where
    #     we cannot rely on blobfuse mapping, and we know we have xtlib installed.
    #     '''

    #     self.append_title(cmds, "UPLOAD service and XT logs to job storage:")

    #     # workaround for "$jobs" not resolving correctly on compute node
    #     job_id = args["job_id"]
    #     workspace = args["workspace"]
    #     jobs_container = store_utils.get_jobs_container(workspace)
    #     store_after = "/{}/jobs/{}/nodes/node{}/after".format(jobs_container, job_id, self.node_index)

    #     if self.gen_for_windows:

    #         # copy from __after__/xt_logs to output node dir
    #         dest = "%XT_NODE_DIR%\\after\\xt_logs"
    #         self.append(cmds, "xcopy {} {}\\".format(constants.WINDOWS_AFTER_LOGS, dest))

    #         # copy node run_errors directory to output node dir
    #         dest = "%XT_NODE_DIR%\\after\\run_errors"
    #         self.append(cmds, "xcopy {} {}\\ /s".format(run_errors.WINDOWS_RUN_ERRORS_DIR, dest))

    #         # have backend add its needed cmds to copy the service logs
    #         dest = "%XT_NODE_DIR%\\after\\service_logs"
    #         self.add_service_log_copy_cmds(cmds, dest, args)         

    #         if not self.mounting_enabled:
    #             # specify workspace since our config file isn't present on the compute node
    #             src_after = "%XT_NODE_DIR%\\after"
    #             self.append(cmds, "xt upload {} {} --feedback=0".format(src_after, store_after))

    #     else:
    #         # debug - why can't we find the LINUX_AFTER_LOGS dir?
    #         # self.append_dir(cmds, ".")
    #         # self.append_dir(cmds, "__after__")
    #         #self.append_dir(cmds, "/usr/src/__after__")
            
    #         # copy from __after__/xt_logs to output node dir
    #         dest = "$XT_NODE_DIR/after/xt_logs"
    #         self.append(cmds, "mkdir -p {}".format(dest))
    #         self.append(cmds, "cp {}/. {}".format(constants.LINUX_AFTER_LOGS, dest))
    #         self.append(cmds, "cp /usr/src/{}/. {}".format(constants.LINUX_AFTER_LOGS, dest))

    #         # copy node run_errors directory to output node dir (but avoid err msg if no files)
    #         dest = "$XT_NODE_DIR/after/run_errors"
    #         self.append(cmds, "find {}/* > /dev/null 2>&1 && mkdir -p {} && cp -r {}/* {}".\
    #             format(run_errors.LINUX_RUN_ERRORS_DIR, dest, run_errors.LINUX_RUN_ERRORS_DIR, dest))

    #         # have backend add its needed cmds to copy the service logs
    #         dest = "$XT_NODE_DIR/after/service_logs"
    #         self.add_service_log_copy_cmds(cmds, dest, args)         

    #         if not self.mounting_enabled:
    #             # if blobfuse is unavailable, we manually upload the logs using XT (assumes XT has been successfully loaded)
    #             src_after = "$XT_NODE_DIR/after"
    #             cmd = "xt upload {} {} --feedback=0".format(src_after, store_after)
    #             self.append(cmds, cmd)

    #         # remove all mounted drives
    #         if self.mounted_drives:
    #             self.append_title(cmds, "Unmount Blobfuse drives")
                
    #             for md in self.mounted_drives:
    #                 self.append(cmds, "fusermount -u -q {} && rm -rf {}".format(md, md))

    #     # if True:
    #     #     # DEBUG: keep each node alive for 7 days for Azure Batch team to debug it
    #     #     self.append(cmds, "sleep 7d")

        
    # def export_now_to_var(self, cmds, var_name):
    #     '''
    #     export current date/time in an arrow-compatible format, including timezone, to specified var_name.
    #     '''

    #     # don't use arrow (early setup - it may not be installed)
    #     #now_cmd = 'python -c "import arrow; print(arrow.now())"'

    #     # don't use datetime (early python versions may not support astimezone() with no arg)
    #     #now_cmd = 'python -c "import datetime; print(datetime.datetime.now().astimezone())"'

    #     # time gives us pretty much what we need (except for fractions of a second)
    #     now_cmd = '''python -c "import time; print(time.strftime('%Y-%m-%d %H:%M:%S.0%z', time.localtime()))"'''

    #     if self.gen_for_windows:
    #         now_cmd = now_cmd.replace("%", "%%")      # windows will strip first "%" away
    #         cmd = "{} > __t__ && set /p {}= < __t__".format(now_cmd, var_name)
    #         self.append(cmds, cmd)   
    #     else:
    #         self.append_export(cmds, var_name, '$({})'.format(now_cmd), fix_value=False)

    # def append_pre_docker_cmds(self, cmds, args):
        
    #     if self.get_name() == "batch":
    #         # run script to extract Azure Batch NODE and POOL ids
    #         # this is done for debugging nodes with Azure Batch team
    #         ws_id = args["workspace"]
    #         job_id = args["job_id"]

    #         # get BATCH credentials
    #         service = self.compute_def["service"]
    #         batch_creds = self.config.get_service(service)
    #         batch_key = batch_creds["key"]
    #         batch_url = batch_creds["url"]

    #         batch_job_id = self.make_batch_job_id(ws_id, job_id)

    #         self.append(cmds, "echo run script to extract Azure Batch NODE and POOL ids > /dev/null")
    #         self.append(cmds, "python {} {} {} {} {} {}".format(constants.FN_BATCH_NODE_ID, batch_job_id, self.node_index, service, batch_url, batch_key))

    #     elif self.get_name() == "singularity":
    #         # on singularity, we must write long env var strings into a separate script
    #         self.append(cmds, "export $(cat {} | xargs)".format(constants.FN_SET_ENV_VARS))


    # def add_reports(self, cmds, report_title, args):

    #     self.append_title(cmds, report_title, True, double=True)

    #     # CMD LINE report (must always do this)
    #     self.append_title(cmds, "CMD LINE report:", True)
    #     #self.append(cmds, "echo 'command line args: $@'")
    #     self.append(cmds, "echo 'dollar1 is $1'")
    #     self.append(cmds, "echo 'dollar2 is $2'")
    #     self.append(cmds, "export XT_DIRECT_CMD=${@:3:999}")
    #     self.append(cmds, "echo 'XT_DIRECT_CMD is $XT_DIRECT_CMD'")

    #     log_reports = args["log_reports"]
    #     if log_reports:

    #         # OS report
    #         self.append_title(cmds, "OS report:", True)
    #         self.append(cmds, "cat /etc/os-release")
    #         self.append(cmds, "cat /etc/motd")

    #         self.append(cmds, "whoami")

    #         # Disk report
    #         self.append_title(cmds, "Disk report:", True)
    #         self.append(cmds, "df -h")

    #         # CPU report
    #         self.append_title(cmds, "CPU report:", True)
    #         self.append(cmds, "lscpu")

    #         # Memory report
    #         self.append_title(cmds, "MEMORY report:", True)
    #         self.append(cmds, "free -mh")

    #         # GPU report
    #         self.append_title(cmds, "GPU report:", True)

    #         # several techinques to show version of NVIDIA DRIVERS
    #         self.append(cmds, "whereis nvidia")

    #         # self.append(cmds, 'grep "X Driver" /var/log/Xorg.0.log')
    #         # self.append(cmds, 'modinfo /usr/lib/modules/$(uname -r)/kernel/drivers/video/nvidia.ko | grep ^version')
    #         #self.append(cmds, "nvcc --version")

    #         # debug nvidia drivers/toolkit combinations
    #         self.append(cmds, "nvidia-smi")

    #         # # TORCH version (is GPU available to torch?)
    #         # target_cmd = '''python -c "import torch; print('PyTorch:'.ljust(15) + ' ' + torch.__version__ + ', CUDA available: ' + str(torch.cuda.is_available()))"'''
    #         # self.append_package_test(cmds, "torch", target_cmd, "PyTorch")

    # def create_wrapper_and_inner(self, cmds, user_cmd, sudo_available, args):

    #     # debug
    #     self.append_dir(cmds)

    #     is_direct_run = self.config.get("general", "direct-run")
    #     if is_direct_run:
    #         self.append_title(cmds, "LAUNCHING USER SCIPT (direct-run=1):")
            
    #         working_dir = args["working_dir"]
    #         if working_dir:
    #             self.append(cmds, "cd {}".format(working_dir))

    #         self.append(cmds, "echo XT_DIRECT_CMD is $XT_DIRECT_CMD")

    #         # run direct cmd
    #         self.append(cmds, "$XT_DIRECT_CMD")
            
    #         self.append_title(cmds, "DIRECT CMD EXITED:")

    #     else:
    #         self.append_title(cmds, "LAUNCHING XT CONTROLLER:")
    #         self.append(cmds, user_cmd)
    #         self.append_title(cmds, "XT CONTROLLER EXITED:")

    #     self.export_now_to_var(cmds, "XT_POST_START_TIME")

    #     docker_cmd = args["docker_cmd"]
    #     timeout = args["docker_pull_timeout"]

    #     # append cmd(s) to download service and xt logs
    #     bootstrap_dir = args["bootstrap_dir"]
    #     self.add_log_upload_cmds(cmds, args)

    #     # log the POST end_time and duration
    #     cmd = 'python -c "from xtlib import node_post_wrapup; node_post_wrapup.main()" '
    #     self.append(cmds, cmd)

    #     self.add_node_sleep_cmd(cmds, args)

    #     #self.append(cmds, ":")     # one last command to give us a timestamp for exit
    #     self.append_title(cmds, 'END of XT-level processing', double=True)

    #     # remove empty cmds
    #     cmds = [cmd for cmd in cmds if cmd]

    #     # construct SLEEP CMD to randomly delay start of node execution
    #     node_count = args["node_count"]
    #     node_delay = args["node_delay"]

    #     if node_delay and node_count > 1:
    #         value = int(utils.shell_time_str_to_secs(node_delay))
    #         sleep_cmd = "sleep $((RANDOM % {}))".format(value)
    #     else:
    #         sleep_cmd = None

    #     # for more reliable and easier-to-debug operation, write cmds to a .sh/.bat file (in bootstrap_dir)
    #     if docker_cmd:
    #         # write docker cmds to WRAPPED script (pool backend)
    #         docker_cmds = []

    #         # we need to generate for our native environment for the docker cmds
    #         self.gen_for_windows = self.is_windows
    #         index = 0

    #         if self.is_windows:
    #             self.append(docker_cmds, "@echo off", echo=False)
    #             index=1

    #         self.append_title(docker_cmds, 'START OF XT-LEVEL PROCESSING (with DOCKER)', double=True, index=index)

    #         if sleep_cmd:
    #             self.append(docker_cmds, sleep_cmd)

    #         self.add_reports(docker_cmds, "before docker reports", args)

    #         self.append_pre_docker_cmds(docker_cmds, args)

    #         if self.get_name() == "batch":
    #             azure_image = utils.safe_value(self.compute_def, "azure-image")
    #             img_dict = self.config.get("azure-batch-images", azure_image)
    #             mount_docker = utils.safe_value(img_dict, "mount-docker")
    #             if mount_docker:
    #                 # move docker files to specified mount point (for nodes where system storage is too small for our docker image)

    #                 docker_path = utils.safe_value(img_dict, "docker-path")
    #                 if not docker_path:
    #                     docker_path = "/var/lib/docker"

    #                 self.append(docker_cmds, "sudo systemctl stop docker")
    #                 self.append(docker_cmds, "sudo mv {} {}-backup".format(docker_path, docker_path))
    #                 self.append(docker_cmds, "sudo mkdir -p {}".format(docker_path))

    #                 self.append(docker_cmds, "sudo mount {} {}".format(mount_docker, docker_path))
    #                 self.append(docker_cmds, "sudo cp -rf {}-backup/. {}".format(docker_path, docker_path))
    #                 self.append(docker_cmds, "sudo systemctl start docker")

    #         # ensure docker is installed and running
    #         install_docker = utils.safe_value(self.compute_def, "install-docker")
    #         if install_docker:
    #             # host OS doesn't have docker, so we must install it

    #             # snap install has problem reading the --env-file (gets permission denied)
    #             # self.append(docker_cmds, "sudo snap install docker")
    #             # self.append(docker_cmds, "sudo snap start docker")

    #             self.append(docker_cmds, "nvcc --version")
    #             self.append(docker_cmds, "sudo docker run hello-world")

    #             self.append(docker_cmds, "curl -fsSL https://get.docker.com -o get-docker.sh")
    #             self.append(docker_cmds, "sudo sh ./get-docker.sh")

    #             self.append(docker_cmds, "sudo docker run hello-world")

    #         else:
    #             # host OS already has docker installed
    #             self.append(docker_cmds, "sudo service docker start ") 

    #         self.append_title(docker_cmds, "START DOCKER CONTAINER:")
    #         self.append_dir(docker_cmds)

    #         login_cmd = args["docker_login_cmd"]
    #         docker_name = args["docker"]
    
    #         self.append(docker_cmds, 'test $(which nvidia-docker) && export DOCKER_RUN="nvidia-docker run"' + 
    #             ' || export DOCKER_RUN="docker run --gpus all"')

    #         self.append(docker_cmds, "echo $DOCKER_RUN")

    #         self.export_now_to_var(docker_cmds, "XT_PULL_START_TIME")

    #         if timeout:
    #             image_name = args["full_docker_image"]
    #             #sudo = "sudo " # if sudo_available else ""

    #             pull_cmds = []
    #             self.append(pull_cmds, 'test $(which nvidia-docker) && export DOCKER_NAME="nvidia-docker"' + 
    #                 ' || export DOCKER_NAME="docker"')

    #             # restart docker service
    #             self.append(pull_cmds, "echo restarting docker service...", echo=False)
    #             self.append(pull_cmds, "sudo systemctl daemon-reload")
    #             self.append(pull_cmds, "sudo systemctl restart docker")

    #             if login_cmd:
    #                 self.append(pull_cmds, login_cmd)

    #             # pull docker image
    #             self.append(pull_cmds, "echo pulling docker image...", echo=False)
    #             self.append(pull_cmds, "sudo $DOCKER_NAME pull {}".format(image_name))

    #             # test docker image by running XT with minimum command
    #             self.append(pull_cmds, "echo testing docker image by running 'xt --version' within it...", echo=False)
    #             self.append(pull_cmds, "sudo $DOCKER_NAME run --rm {} xt --version".format(image_name))

    #             # write PULL CMDS to FN_DOCKER_PULL_SH
    #             fn_wrapped = self.write_cmds_to_file(pull_cmds, bootstrap_dir, self.is_windows, constants.FN_DOCKER_PULL_BAT, constants.FN_DOCKER_PULL_SH)
    #             utils.copy_to_submit_logs(args, fn_wrapped)

    #             pull_cmd = '''timeout {} bash -c "until bash {}; do '''.format(timeout, constants.FN_DOCKER_PULL_SH) + \
    #                 '''echo XT: docker pull+test failed.  retrying...; sleep 60; done" '''

    #             self.append(docker_cmds, pull_cmd)
    #             self.append(docker_cmds, "docker_pull_status=$?", echo=False)
    #             self.append(docker_cmds, "if [ $docker_pull_status -ne 0 ]; then", echo=False)
    #             self.append(docker_cmds, 'echo "XT: ERROR - docker pull TIMED OUT; job aborted"', echo=False)
    #             self.append(docker_cmds, "else", echo=False)
    #             self.append(docker_cmds, 'echo "XT: docker pull+test SUCCEEDED!"', echo=False)
    #             self.append(docker_cmds, docker_cmd)
    #             self.append(docker_cmds, "fi", echo=False)

    #         else:
    #             # not using TIMEOUT option
    #             if login_cmd:
    #                 self.append(docker_cmds, login_cmd)

    #             if not self.is_windows:
    #                 # NOTE: we must set DOCKER_RUN before we can execute docker_cmd
    #                 # different versions of docker require different approaches
    #                 self.append(docker_cmds, docker_cmd)

    #         fn_wrapped = self.write_cmds_to_file(docker_cmds, bootstrap_dir, self.is_windows, constants.FN_WRAPPED_BAT, constants.FN_WRAPPED_SH)
    #         utils.copy_to_submit_logs(args, fn_wrapped)

    #         # write normal cmds to INNER script
    #         fn_inner = self.write_cmds_to_file(cmds, bootstrap_dir, False, constants.FN_INNER_BAT, constants.FN_INNER_SH)
    #         utils.copy_to_submit_logs(args, fn_inner)

    #         # finally, write the full name of the docker image to a special file
    #         fn_image = os.path.join(bootstrap_dir, constants.FN_IMAGE_NAME)
    #         docker_image, login_server, _, _ = self.config.get_docker_info(self.compute, docker_name, required=False)
    #         full_image_name = login_server + "/" + docker_image if login_server and login_server != "docker.io" else docker_image

    #         file_utils.write_text_file(fn_image, full_image_name)
    #     else:
    #         # docker not being used
    #         # write normal cmds to WRAPPED script
    #         #insert_index = 1 if self.gen_for_windows else 0
    #         pre_cmds = []
    #         self.append_title(pre_cmds, 'START of XT-level processing (without DOCKER)', double=True)
    #         if sleep_cmd:
    #             self.append(pre_cmds, sleep_cmd)

    #         # add pre-docker commands without using docker
    #         self.append_pre_docker_cmds(pre_cmds, args)
    #         if self.gen_for_windows:
    #             cmds = [ cmds[0] ] + pre_cmds + cmds[1:]
    #         else:
    #             cmds = pre_cmds + cmds

    #         fn_wrapped = self.write_cmds_to_file(cmds, bootstrap_dir, self.is_windows, constants.FN_WRAPPED_BAT, constants.FN_WRAPPED_SH)
    #         utils.copy_to_submit_logs(args, fn_wrapped)

    #     # remember where we wrote the wrapped file
    #     self.fn_wrapped = fn_wrapped
    #     return fn_wrapped

    # def add_node_sleep_cmd(self, cmds, args):
    #     sleep_on_exit = args["sleep_on_exit"]
    
    #     if sleep_on_exit:
    #         self.append_title(cmds, 'sleeping on exit...', double=True)
    #         self.append(cmds, "sleep {}".format(sleep_on_exit))

    # def write_cmds_to_file(self, cmds, bootstrap_dir, for_windows, fn_bat, fn_sh):
    #     if for_windows:
    #         fn_path = bootstrap_dir + "/" + fn_bat
    #         scriptor.write_script_file(cmds, fn_path, True)
    #     else:
    #         fn_path = bootstrap_dir + "/" + fn_sh
    #         scriptor.write_script_file(cmds, fn_path, False)

    #     return fn_path

    # def get_controller_run_cmd(self, external_controller_port=constants.CONTROLLER_PORT, is_aml=False, multi_run_hold_open=False):

    #     if self.gen_for_windows:
    #         text = '''python -u -c "from xtlib.controller import run; run(port={}, is_aml={}, multi_run_hold_open={})" '''
    #     else:
    #         # linux needs these escapes around the double quotes
    #         text = '''python -u -c 'from xtlib.controller import run; run(port={}, is_aml={}, multi_run_hold_open={})'  '''

    #     cmd = text.format(external_controller_port, is_aml, multi_run_hold_open)
    #     return cmd

    # def add_pip_packages(self, cmds, pip_packages, use_legacy_resolver=False):
    #     if pip_packages:
    #         cmd = "pip install" if self.gen_for_windows else "pip install --user"
    #         if use_legacy_resolver:
    #             cmd += " --use-deprecated=legacy-resolver"

    #         # NOTE: double quotes around package names cause error on linux
    #         for pp in pip_packages:
    #             cmd += ' {}'.format(pp)
    #         self.append(cmds, cmd, log="pip_install")

    # def add_conda_packages(self, cmds, conda_packages):
    #     if conda_packages:
    #         cmd = "conda install"
    #         # NOTE: double quotes around package names cause error on linux
    #         for cp in conda_packages:
    #             cmd += ' {}'.format(cp)
    #         self.append(cmds, cmd, log="conda_install")


    # def cd_back_to_setup_dir(self, cmds):
    #     #cd back to setup directory 
    #     if self.gen_for_windows:
    #         self.append(cmds, "cd %XT_CWD%")
    #     else:
    #         self.append(cmds, "cd $XT_CWD")

    # def add_setup_cmds(self, cmds, remove_zip=True, gen_for_windows=False, args=None):

    #     pre_cmds = args["pre_cmds"]
    #     if pre_cmds:
    #         self.append_title(cmds, "USER pre-setup commands:")
    #         for cmd in pre_cmds:
    #             self.append(cmds, cmd)

    #         self.cd_back_to_setup_dir(cmds)

    #     # KISS: just insist that user specify PYTHONPATH in SETUP (not env vars)
    #     preserve_python_path=False

    #     if preserve_python_path:
    #         self.append_python_path(cmds)
    #         self.append_export(cmds, "BEFORE_PYTHONPATH", "$PYTHONPATH")

    #     self.append_title(cmds, "INSTALL CONDA/PIP packages:")

    #     if remove_zip:
    #         if self.gen_for_windows:
    #             self.append(cmds, "del {}".format(constants.CODE_ZIP_FN))
    #         else:
    #             self.append(cmds, "rm {}".format(constants.CODE_ZIP_FN))

    #     activate_cmd = self.get_activate_cmd(args)
    #     if activate_cmd:
    #         if self.gen_for_windows and not activate_cmd.startswith("call"):
    #             activate_cmd = "call " + activate_cmd  
    #         self.append(cmds, activate_cmd, log="activate_cmd")

    #     pip_freeze = args["pip_freeze"]
    #     if pip_freeze:
    #         self.append(cmds, "pip freeze", log="initial_pip_freeze")

    #     # we use pip install --local, so add it to the path
    #     if self.gen_for_windows:
    #         #self.append(cmds, 'set PATH=%HOME%/.local/bin;%PATH%')
    #         pass
    #     else:
    #         self.append_export(cmds, "PATH", "$HOME/.local/bin:$PATH")

    #     # install CONDA-PACKAGES
    #     conda_packages = args["conda_packages"]
    #     if conda_packages:
    #         self.add_conda_packages(cmds, conda_packages)

    #     # install PIP-PACKAGES (xtlib and user-specified others)
    #     pip_packages = args["pip_packages"]
    #     if pip_packages:
    #         use_legacy_resolver = args["use_legacy_resolver"]
    #         self.add_pip_packages(cmds, pip_packages, use_legacy_resolver)

    #     if pip_freeze:
    #         self.append(cmds, "pip freeze", log="final_pip_freeze")

    #     self.add_xt_setup_cmds(cmds, args)

    #     if preserve_python_path:
    #         self.append_export(cmds, "PYTHONPATH", "$PYTHONPATH:$BEFORE_PYTHONPATH")
    #         self.append_python_path(cmds)

    # def add_xt_setup_cmds(self, cmds, args):
    #     # add "." to PYTHONPATH so that any run of xt.exe will pick up latest XTLIB and USER LIBS
    #     pp = args["python_path"]     # a list of strings from SETUP in config file

    #     if not pp:
    #         # by default, we add XT_CWD to path so xtlib and other libraries usually just work
    #         self.append_export(cmds, "PYTHONPATH", "$XT_CWD")
    #     else:
    #         # user has specified the PYTHONPATH; give them complete control
    #         pp_str = ":".join(pp)
    #         path = file_utils.fix_slashes(pp_str, is_linux=not self.gen_for_windows, protect_ws_run_name=False)
    #         self.append_export(cmds, "PYTHONPATH", path)

    #     self.append_python_path(cmds)

    # API call
    def get_node_status(self, service_node_info):
        pass

    # API call
    def read_log_file(self, service_node_info, log_name, start_offset=0, end_offset=None, 
        encoding='utf-8', use_best_log=True, log_source=None):
        pass

    # API call
    def get_simple_status(self, status):
        # translates an Philly status to a simple status (queued, running, completed)
        pass

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        pass
    
    # API call
    def cancel_node(self, service_node_info):            
        pass

    # API call
    def get_service_queue_entries(self, service_node_info):
        pass

    # helper
    def download_log(self, items, service_node_info, log_name, dest_dir, service_context=None):

        result = self.read_log_file(service_node_info, log_name, service_context=None)  # service_context)
        found_file = utils.safe_value(result, "found_file")

        text = result["new_text"]
        if text or found_file:
            base_log_name = os.path.basename(log_name)
            console.print("found log: {}".format(base_log_name))

            fn_log = "{}/{}".format(dest_dir, base_log_name)
            file_utils.write_text_file(fn_log, text)
            items.append(fn_log)
        return result

    # API call
    def add_service_log_copy_cmds(self, ca, cmds, dest_dir, args):
        pass        