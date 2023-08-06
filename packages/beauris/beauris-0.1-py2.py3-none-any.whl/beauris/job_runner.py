import json
import logging
import os
import time
from datetime import date
from subprocess import PIPE, Popen

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.datasets import TimeoutException

try:
    import drmaa
    from drmaa.errors import ExitTimeoutException
    drmaa_available = True
except RuntimeError:
    drmaa_available = False

from .util import show_logs

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

DRMAA_WRAPPER = """#!/bin/bash

{env}

{cmd}
"""


class Runners():
    def __init__(self, job_specs):
        self.runners = {
            'local': LocalRunner,
            'drmaa': DrmaaRunner,
            'galaxy': GalaxyRunner,
            'nextflow': NextflowRunner,
        }

        self.job_specs = job_specs

    def get(self, name, entity, task_id, server=""):

        if name in self.runners:
            return self.runners[name](self.job_specs, entity, task_id, server)

        raise RuntimeError('Could not find runner named "%s"' % name)


class Runner():

    def __init__(self, job_specs, entity, task_id, server=""):

        self.task = entity.tasks[task_id]

        self.job_specs = job_specs

        self.name = None

    def get_job_specs(self, task_id):

        return self.job_specs[self.name][task_id] if self.name in self.job_specs and task_id in self.job_specs[self.name] else {}

    def run_or_resume_job(self, check_output=True, since='last_lock', **kwargs):

        if self.task.disable_run():
            log.info("Task {} execution is disabled by tags, skipping.".format(self.task.name))
            return 0, '', ''

        if not self.task.needs_to_run(since=since):
            # Using since=last_run would return true when there was a run (forced or because of a change in input file revision),
            # then the force tag was removed or revision was switched back to old value. We don't want that.
            log.info("No change in file(s) we depend on for task {} since {}, skipping.".format(since, self.task.name))
            return 0, '', ''

        exit_code, out, err, has_already_run = self.check_previous_run(**kwargs)

        exit_code = self.task.get_previous_exit_code()

        if not has_already_run or self.task.force_run():
            exit_code, out, err = self.run_job(**kwargs)
            show_logs(out, err)

        if check_output:
            exit_code += self.task.check_expected_outputs()

        return exit_code, out, err

    def run_job(self, **kwargs):
        """
        Runs a job with this runner

        Returns
            - the exit code
            - stdout
            - stderr
        """

        # We run a job, get rid of any trace left by a previous run
        self.task.clear_exit_code()
        self.task.clear_previous_logs()
        self.task.clear_jobid()

        # Save the current state of input data
        self.task.save_data_state()

        # We're really running something
        self.task.has_run = True

        # Subclasses are supposed to run their code here now

    def check_previous_run(self, **kwargs):

        last_exit_code = self.task.get_previous_exit_code()

        last_out, last_err = self.task.get_previous_logs()

        has_already_run = False

        if not self.task.deps_have_changed(since='last_run') and not self.task.force_run():

            if last_exit_code is not None:

                # It ran and we have an exit code, no need to rerun

                has_already_run = True

                if last_exit_code == 0:
                    log.info("Skipping {}, already succeeded previously".format(self.task.name))
                else:
                    log.info("Skipping {}, already failed previously with the following log:".format(self.task.name))
                    last_out, last_err = self.task.get_previous_logs()
                    show_logs(last_out, last_err)

        return last_exit_code, last_out, last_err, has_already_run


class LocalRunner(Runner):

    def __init__(self, job_specs, entity, task_id, server=""):
        Runner.__init__(self, job_specs, entity, task_id, server)

        self.name = 'local'

    def run_job(self, cmd=None, **kwargs):

        if cmd is None:
            raise RuntimeError("Cannot run job, param cmd is empty")

        Runner.run_job(self)

        log.info("Running locally: {}".format(cmd))
        cmd_env = os.environ.copy()
        cmd_env.update({'PYTHONUNBUFFERED': '1'})
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, env=cmd_env)
        output, err = p.communicate()
        retcode = p.returncode

        self.task.save_exit_code(retcode)

        self.task.save_logs(output, err)

        return retcode, output, err


class AsyncRunner(Runner):

    def __init__(self, job_specs, entity, task_id, server=""):
        Runner.__init__(self, job_specs, entity, task_id, server)

    def check_previous_run(self, dest_rename={}, **kwargs):

        last_exit_code = self.task.get_previous_exit_code()

        last_out, last_err = self.task.get_previous_logs()

        last_jobid = self.task.get_previous_jobid()

        task_work_dir = self.task.get_work_dir()

        is_running = False

        if last_jobid:
            log.info("Found an existing jobid from a previous run: {}".format(last_jobid))
            is_running = self.is_job_running(last_jobid)

        has_already_run = False

        if not self.task.deps_have_changed(since='last_run') and not self.task.force_run():

            if is_running:

                # It's still running, wait for it and grab results
                self.task.has_run = True

                log.info("Job {} is still running, waiting for it".format(last_jobid))
                last_exit_code = self.wait_for_job(last_jobid)

                last_out, last_err = self.fetch_logs(last_jobid)

                self.task.save_exit_code(last_exit_code)

                self.task.save_logs(last_out, last_err)

                show_logs(last_out, last_err)

                self.fetch_results(last_jobid, task_work_dir, dest_rename)

                has_already_run = True

            elif last_exit_code is not None:

                log.info("Job {} is no longer running, and data has not changed, checking the last run result.".format(last_jobid))

                has_already_run = True

                if last_exit_code == 0:
                    log.info("Skipping {}, already succeeded previously".format(self.task.name))

                    self.fetch_results(last_jobid, task_work_dir, dest_rename, only_new=True)
                else:
                    log.info("Skipping {}, already failed previously with the following log:".format(self.task.name))
                    last_out, last_err = self.task.get_previous_logs()
                    show_logs(last_out, last_err)
            else:
                log.warning("Job {} is no longer running, but could not find its exit code. There's a bug somewhere probably.".format(last_jobid))

        elif is_running:

            rerun_reason = "forced to rerun"
            if self.task.deps_have_changed(since='last_run'):
                rerun_reason = "data as changed"

            log.info("Job {} is still running, but {}, will kill it and launch a new job".format(last_jobid, rerun_reason))
            # Data has changed but job is still running on old data, kill the running job
            self.kill_job(last_jobid)

            # Save exit code and logs just in case, but will be erased by the next run_job call
            exit_code = self.wait_for_job(last_jobid)

            last_out, last_err = self.fetch_logs(last_jobid)

            self.task.save_exit_code(exit_code)

            self.task.save_logs(last_out, last_err)

        return last_exit_code, last_out, last_err, has_already_run

    def wait_for_job(self, jobid, timeout=None):

        raise NotImplementedError()

    def is_job_running(self, jobid):

        raise NotImplementedError()

    def kill_job(self, jobid):

        raise NotImplementedError()

    def fetch_logs(self, jobid):

        raise NotImplementedError()

    def fetch_results(self, jobid, dest_dir, dest_rename={}, only_new=False):

        # Only needed when results need to be downloaded
        pass


class DrmaaRunner(AsyncRunner):

    def __init__(self, job_specs, entity, task_id, server=""):

        if not drmaa_available:
            raise RuntimeError("Could not load drmaa python module, you can't use the DRMAA runner")

        Runner.__init__(self, job_specs, entity, task_id, server)

        self.name = 'drmaa'

    def run_job(self, script_path=None, job_args=[], **kwargs):

        if script_path is None:
            raise RuntimeError("Cannot run job, param script_path is empty")

        job_name = self.task.slug()

        task_work_dir = self.task.get_work_dir()

        Runner.run_job(self)

        specs = self.get_job_specs(self.task.specs_id)

        nativ_specs = specs['native_specification'] if 'native_specification' in specs else ""
        job_env = specs['env'] if 'env' in specs else ""

        with drmaa.Session() as s:
            # We create a wrapper script to inject env from job_specs without touching
            wrapper_path = os.path.join(task_work_dir, job_name + ".sh")
            cmd = script_path + " " + " ".join(job_args)
            log.info('Preparing job wrapper script {}'.format(wrapper_path))
            log.info('Will execute command: {}'.format(cmd))
            with open(wrapper_path, 'w') as wrapper:
                wrapper.write(DRMAA_WRAPPER.format(env=job_env, cmd=cmd))
            os.chmod(wrapper_path, 0o744)

            log.info('Creating DRMAA job template')
            jt = s.createJobTemplate()
            jt.remoteCommand = wrapper_path

            jt.jobName = job_name
            jt.workingDirectory = task_work_dir

            if nativ_specs:
                jt.nativeSpecification = " " + nativ_specs

            jt.args = job_args

            is_slurm_implementation = "slurm" in s.drmaaImplementation.lower()

            if is_slurm_implementation:
                jt.outputPath = ":" + os.path.join(task_work_dir, "{}.o%A".format(job_name))
                jt.errorPath = ":" + os.path.join(task_work_dir, "{}.e%A".format(job_name))
            else:
                jt.outputPath = ":" + os.path.join(task_work_dir)
                jt.errorPath = ":" + os.path.join(task_work_dir)

            jobid = s.runJob(jt)
            s.deleteJobTemplate(jt)

        log.info('Your job has been submitted with ID %s' % jobid)
        self.task.save_jobid(jobid)

        exit_code = self.wait_for_job(jobid)

        stdout, stderr = self.fetch_logs(jobid)

        self.task.save_exit_code(exit_code)

        self.task.save_logs(stdout, stderr)

        return exit_code, stdout, stderr

    def wait_for_job(self, jobid, timeout=None):

        first_try = True
        retry = timeout is None
        if timeout is None:
            # Default timeout
            timeout = 3600

        with drmaa.Session() as s:

            while first_try or retry:
                log.info('Waiting for job with ID %s' % jobid)

                try:
                    retval = s.wait(str(jobid), timeout)
                    retry = False
                except ExitTimeoutException:
                    if not retry:
                        raise

                first_try = False

            # No exception = job is finished
            log.info('Job: {0} finished with status {1}'.format(jobid, retval.exitStatus))

        return retval.exitStatus

    def is_job_running(self, jobid):

        with drmaa.Session() as s:
            status = s.jobStatus(str(jobid))

        return status not in [drmaa.JobState.DONE, drmaa.JobState.FAILED]

    def kill_job(self, jobid):

        with drmaa.Session() as s:
            s.control(str(jobid), drmaa.JobControlAction.TERMINATE)

        # Wait a little for confirmation
        tries = 10
        while tries > 0:
            if self.is_job_running(jobid):
                time.sleep(3)
            else:
                tries = 0

    def fetch_logs(self, jobid):

        with drmaa.Session() as s:
            is_slurm_implementation = "slurm" in s.drmaaImplementation.lower()

        work_dir = self.task.get_work_dir()
        job_name = self.task.slug()

        stdout = ""
        stderr = ""
        if not is_slurm_implementation:
            non_slurm_logs = os.path.join(work_dir, "slurm-{}.out".format(jobid))
            if os.path.isfile(non_slurm_logs):
                with open(non_slurm_logs, 'r') as fh_log:
                    stdout = fh_log.read()
        else:
            slurm_out = "{}/{}.o{}".format(work_dir, job_name, jobid)
            slurm_err = "{}/{}.e{}".format(work_dir, job_name, jobid)
            if os.path.isfile(slurm_out):
                with open(slurm_out, 'r') as fh_log:
                    stdout = fh_log.read()
            if os.path.isfile(slurm_err):
                with open(slurm_err, 'r') as fh_log:
                    stderr = fh_log.read()

        return stdout, stderr


class GalaxyRunner(AsyncRunner):

    def __init__(self, job_specs, entity, task_id, server=""):

        Runner.__init__(self, job_specs, entity, task_id, server)

        self.name = 'galaxy'

        self.final_states = ['ok', 'error', 'failed', 'deleted']

        self.history_id = None

        # TODO get this from beauris.yml
        self.gi = GalaxyInstance(os.getenv('GALAXY_URL'), os.getenv('GALAXY_API_KEY'))

    def run_job(self, tool=None, params={}, uploads={}, dest_rename={}, **kwargs):

        if tool is None:
            raise RuntimeError("Cannot run job, param tool is empty")

        history_name = "{}_{}".format(date.today(), self.task.slug())

        Runner.run_job(self)

        if tool.startswith('toolshed.g'):
            tool_id = tool
        else:
            tool_id = self.get_tool(tool)

        log.info("Will run tool {} on Galaxy server {}".format(tool_id, os.getenv('GALAXY_URL')))

        log.info("Using params: {}".format(params))

        # Not storing history id, 1 history per execution (=runner instance lifetime)
        history_id = self.get_history(history_name)

        params = self.upload_files(history_name, uploads, params)

        tool_invocation = self.gi.tools.run_tool(history_id, tool_id, params)

        job_id = tool_invocation['jobs'][0]['id']

        log.info('Your job has been submitted with ID %s' % job_id)
        self.task.save_jobid(job_id)

        exit_code = self.wait_for_job(job_id)

        stdout, stderr = self.fetch_logs(job_id)

        self.task.save_exit_code(exit_code)

        self.task.save_logs(stdout, stderr)

        dest_dir = self.task.get_work_dir()
        self.fetch_results(job_id, dest_dir, dest_rename)

        return exit_code, stdout, stderr

    def get_history(self, name=None):

        if self.history_id:
            return self.history_id

        new_hist = self.gi.histories.create_history(name=name)

        log.info('Created a new history named {}'.format(new_hist['name']))

        self.history_id = new_hist['id']

        return self.history_id

    # TODO use a fixed version or latest?
    def get_tool(self, tool_name):

        tools = self.gi.tools.get_tools(name=tool_name)
        if not tools:
            raise RuntimeError("Cannot find tool {}".format(tool_name))

        # Sort by id (newest will end up at the end hopefully)
        tools = sorted(tools, key=lambda d: d['id'])

        return tools[-1]['id']

    def upload_files(self, history_name, uploads, params):

        params_str = json.dumps(params)

        for id, infos in uploads.items():
            upload_id = self.upload_file(history_name, infos['path'], file_name=infos['name'], file_type=infos['type'])

            params_str = params_str.replace("##UPLOADED_DATASET_ID__{}##".format(id), upload_id)

        return json.loads(params_str)

    def upload_file(self, history_name, dataset, file_name=None, file_type=None):

        history_id = self.get_history(history_name)

        args = {
            'path': dataset,
            'history_id': history_id,
        }

        if file_name:
            args['file_name'] = file_name

        if file_type:
            args['file_type'] = file_type

        dataset = self.gi.tools.upload_file(**args)

        return dataset['outputs'][0]['id']

    def wait_for_job(self, jobid, timeout=None):

        first_try = True
        retry = timeout is None
        if timeout is None:
            # Default timeout
            timeout = 3600

        while first_try or retry:
            log.info('Waiting for job with ID %s' % jobid)

            try:
                self.gi.jobs.wait_for_job(jobid, interval=30, check=False)
                retry = False
            except TimeoutException:
                if not retry:
                    raise

            first_try = False

        state = self.gi.jobs.get_state(jobid)

        if state == 'ok':
            exit_code = 0
        else:
            # TODO we could get exit_code from the tool execution, but not sure if it's always coherent with the job state
            # (=maybe we can get a 0 ecit code while the job looks ok?)
            exit_code = 1

        # No exception = job is finished
        log.info('Job: {0} finished with status {1}'.format(jobid, exit_code))

        return exit_code

    def is_job_running(self, jobid):

        state = self.gi.jobs.get_state(jobid)

        return state not in self.final_states

    def kill_job(self, jobid):

        return self.gi.jobs.cancel_job(jobid)

    def fetch_logs(self, jobid):

        job_info = self.gi.jobs.show_job(jobid, full_details=True)

        return job_info['stdout'], job_info['stderr']

    def fetch_results(self, jobid, dest_dir, dest_rename={}, only_new=False):

        outputs = self.gi.jobs.get_outputs(jobid)

        for out in outputs:
            need_rename = out['name'] in dest_rename
            dest = os.path.join(dest_dir, dest_rename[out['name']]) if need_rename else dest_dir

            if only_new and need_rename and os.path.exists(dest):
                log.info("Dataset {} already downloaded previously in {}".format(out['dataset']['id'], dest))
            else:
                log.info("Downloading dataset {} in {}".format(out['dataset']['id'], dest))
                self.gi.datasets.download_dataset(out['dataset']['id'], dest, use_default_filename=not need_rename)

        self.delete_history(jobid)

    def delete_history(self, jobid):

        job_infos = self.gi.jobs.show_job(jobid)

        hid = job_infos['history_id']

        self.gi.histories.delete_history(hid, purge=True)


class NextflowRunner(AsyncRunner):

    def __init__(self, job_specs, entity, task_id, server=""):

        Runner.__init__(self, job_specs, entity, task_id, server)

        self.name = 'netxflow'

    def run_job(self, **kwargs):

        Runner.run_job(self)

        raise NotImplementedError()
