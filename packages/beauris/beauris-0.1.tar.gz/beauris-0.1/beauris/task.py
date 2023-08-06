import json
import logging
import os

from .util import Util, file_state

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class TaskOutput():
    def __init__(self, name, ftype, path, tool_version=None, publish=True, depends_on=[]):

        self.name = name
        self.ftype = ftype
        self.path = path  # The path of the output file relative to the task workdir
        self.publish = publish
        self.tool_version = tool_version  # TODO get this from config/job_specs or by parsing output files
        self.depends_on = depends_on


class Task():

    def __init__(self, entity, name, depends_on=[], check_perms=False, specs_id="", workdir="", always_run=False, server=""):

        if workdir:
            self.workdir = workdir
        else:
            self.workdir = name
            if server:
                self.workdir += "_{}".format(server)

        self.specs_id = specs_id if specs_id else name

        self.name = name
        self.entity = entity

        self.server = server

        # TODO changing access restriction will trigger all tasks, maybe we could limit to only triggering deploy tasks in this case ?
        self.check_perms = check_perms

        # Sometimes a task depends on some intput/derived files, but will not generate any derived file
        # In this case, you can define dependencies at the task level instead of doing it on a derived file
        self.depends_on = depends_on

        # True when the task has been run (not in a previous run, just now)
        self.has_run = False

        # True if a task should always run, whatever the state of dependencies
        self.always_run = always_run

    def get_derived_outputs(self, entity):
        """
        Returns a dict of derived files produced by current task
        """

        return []

    def slug(self, short=True):

        slug = "{}_{}".format(self.name, self.entity.slug(short=short))

        if self.server:
            slug += "_{}".format(self.server)

        return slug

    def get_work_dir(self):

        return os.path.join(self.entity.get_work_dir(), self.workdir)

    def create_work_dir(self):

        os.makedirs(self.get_work_dir(), exist_ok=True)

    def get_previous_exit_code(self):

        exit_code_path = os.path.join(self.get_work_dir(), "{}.exit_code".format(self.name))
        last_exit_code = None
        if os.path.isfile(exit_code_path):
            with open(exit_code_path, 'r') as fh_exit_code:
                try:
                    last_exit_code = int(fh_exit_code.readline().strip())
                except ValueError:
                    last_exit_code = None

        return last_exit_code

    def save_exit_code(self, exit_code):

        exit_code_path = os.path.join(self.get_work_dir(), "{}.exit_code".format(self.name))

        with open(exit_code_path, 'w') as fh_exit_code:
            fh_exit_code.write(str(exit_code))

    def clear_exit_code(self):

        exit_code_path = os.path.join(self.get_work_dir(), "{}.exit_code".format(self.name))

        if os.path.exists(exit_code_path):
            os.remove(exit_code_path)

    def save_jobid(self, jobid):

        jobid_path = os.path.join(self.get_work_dir(), "{}.jobid".format(self.name))

        with open(jobid_path, 'w') as fh_jobid:
            fh_jobid.write(str(jobid))

    def clear_jobid(self):

        jobid_path = os.path.join(self.get_work_dir(), "{}.jobid".format(self.name))

        if os.path.exists(jobid_path):
            os.remove(jobid_path)

    def get_previous_jobid(self):

        jobid_path = os.path.join(self.get_work_dir(), "{}.jobid".format(self.name))
        last_jobid = None
        if os.path.isfile(jobid_path):
            with open(jobid_path, 'r') as fh_jobid:
                try:
                    last_jobid = fh_jobid.readline().strip()
                except ValueError:
                    last_jobid = None

        return last_jobid

    def save_logs(self, out, err):
        """
        Save stdout and stderr from str variables into files in work dir
        """

        out_path = os.path.join(self.get_work_dir(), "{}.out".format(self.name))
        err_path = os.path.join(self.get_work_dir(), "{}.err".format(self.name))

        with open(out_path, 'w') as outh:
            outh.write(out)

        with open(err_path, 'w') as errh:
            errh.write(err)

    def get_previous_logs(self):

        last_out = self._get_previous_log('out')
        last_err = self._get_previous_log('err')

        return last_out, last_err

    def _get_previous_log(self, type):

        if type not in ('out', 'err'):
            raise Exception('Only "out" and "err" are allowed, not {}'.format(type))

        log_path = os.path.join(self.get_work_dir(), "{}.{}".format(self.name, type))
        last_log = None
        if os.path.isfile(log_path):
            with open(log_path, 'r') as fh_log:
                last_log = fh_log.read()

        return last_log

    def clear_previous_logs(self):

        out_path = os.path.join(self.get_work_dir(), "{}.out".format(self.name))
        err_path = os.path.join(self.get_work_dir(), "{}.err".format(self.name))

        if os.path.exists(out_path):
            os.remove(out_path)

        if os.path.exists(err_path):
            os.remove(err_path)

    def save_data_state(self):

        current_state = self.get_data_state()

        with open(os.path.join(self.get_work_dir(), '{}.state'.format(self.name)), 'w') as state_f:
            json.dump(current_state, state_f, indent=4, sort_keys=True)

    def load_previous_data_state(self):

        path = os.path.join(self.get_work_dir(), '{}.state'.format(self.name))

        if not os.path.isfile(path):
            return {}

        with open(path, 'r') as state_f:
            return json.load(state_f)

    def force_run(self):

        labels = Util.mr_labels

        return self.always_run or 'run-everything' in labels or 'run-{}'.format(self.name) in labels or 'run-{}'.format(self.specs_id) in labels or 'run-{}_{}'.format(self.name, self.server) in labels

    def disable_run(self):

        labels = Util.mr_labels

        return 'disable-everything' in labels or 'disable-{}'.format(self.name) in labels or 'disable-{}'.format(self.specs_id) in labels or 'disable-{}_{}'.format(self.name, self.server) in labels

    def get_data_state(self):

        state = {}

        state['entity'] = self.entity.slug()

        if self.check_perms:
            state['restricted_to'] = self.entity.get_organism().restricted_to

        dep_num = 0

        for id, exp_res in self.entity.derived_files.items():

            if exp_res.task.name != self.name or exp_res.task.server != self.server:
                continue

            for res_dep in exp_res.depends_on:
                state["{}_{}".format(dep_num, res_dep.name)] = file_state(res_dep.get_usable_path())
                dep_num += 1

        for res_dep in self.depends_on:
            state["{}_{}".format(dep_num, res_dep.name)] = file_state(res_dep.get_usable_path())
            dep_num += 1

        return state

    def deps_have_changed_since_last_run(self):

        current_state = self.get_data_state()

        # Make sure current_state is sorted like previous one
        current_state = json.dumps(current_state, indent=4, sort_keys=True)
        current_state = json.loads(current_state)

        previous_state = self.load_previous_data_state()

        return current_state != previous_state

    def deps_have_changed_since_last_lock(self):

        if self.check_perms:
            current_perms = self.entity.get_organism().restricted_to
            locked_perms = self.entity.get_organism().locked_restricted_to

            if current_perms != locked_perms:
                return True

        for id, exp_res in self.entity.derived_files.items():

            if exp_res.task.name != self.name or exp_res.task.server != self.server:
                continue

            for res_dep in exp_res.depends_on:
                if res_dep.has_changed_since_last_lock():
                    log.debug("Dep {} has changed since last lock for {}".format(res_dep.name, exp_res.name))
                    return True
                log.debug("No change since last lock in dep {} for {}".format(res_dep.name, exp_res.name))

        for res_dep in self.depends_on:
            if res_dep.has_changed_since_last_lock():
                log.info("Task dep {} has changed since last lock".format(res_dep.name))
                return True
            log.debug("No change since last lock in task dep {}".format(res_dep.name))

        return False

    def deps_have_changed(self, since='last_run'):

        if since == 'last_run':
            return self.deps_have_changed_since_last_run()
        elif since == 'last_lock':
            return self.deps_have_changed_since_last_lock()
        else:
            raise Exception("Unexpected 'since' parameter to deps_have_changed()")

    def check_expected_outputs(self):

        found = 0
        missing = 0

        for id, exp in self.entity.derived_files.items():

            if exp.task.name != self.name or exp.task.server != self.server:
                continue

            if not exp.file_exists():
                log.error("  ❌ Did not find expected output {} for task {}: {}".format(id, self.name, exp.path))
                missing += 1
            else:
                log.info("  ✅ Found expected output {} for task {}: {}".format(id, self.name, exp.path))
                found += 1

        if found == 0 and missing == 0:
            log.info("Not expecting any output file for task {}".format(self.name))
            return missing

        return missing

    def derived_files_exist(self, locked=False):

        for id, exp in self.entity.derived_files.items():

            if exp.task.name != self.name or exp.task.server != self.server:
                continue

            if not exp.file_exists(locked=locked):
                return False

        return True

    def needs_to_run(self, since='last_lock'):

        changed = self.deps_have_changed(since=since)

        if self.disable_run():
            log.debug("Task {} is disabled by labels".format(self.name))

        elif self.force_run():
            log.debug("Task {} is forced to run by labels".format(self.name))

        elif changed:
            log.debug("Task {} needs to run because of changed dependencies".format(self.name))

        elif not self.derived_files_exist(locked=True):
            log.debug("Task {} needs to run because of missing derived files".format(self.name))

        # This could be cached in most cases, but it would made testing awkward
        needs_to_run = not self.disable_run() and (self.force_run() or changed or not self.derived_files_exist(locked=True))

        return needs_to_run
