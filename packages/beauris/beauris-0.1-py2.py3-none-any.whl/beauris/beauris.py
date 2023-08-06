import logging

from .config import Config
from .data_locker import DataLockers
from .job_runner import Runners
from .organism import Organism

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Beauris():

    def __init__(self, root_work_dir=None, config_file=None):

        self.config = Config(root_work_dir, config_file)

        self.runners = Runners(self.config.job_specs)

        self.data_lockers = DataLockers()

    def load_organism(self, yml_path, test_data=False, locked_dir=None, future_locked_dir=None):

        return Organism(self.config, yml_path, test_data=test_data, locked_dir=locked_dir, future_locked_dir=future_locked_dir, default_services=self.config.deploy_services)

    def get_runner(self, method, entity, task_id, server=""):

        return self.runners.get(method, entity, task_id, server)

    def get_data_locker(self, override_conf={}):

        method = self.config.raw['data_locker']['method']

        locker_conf = self.config.raw['data_locker']['options']

        # This is used mainly for tests
        locker_conf.update(override_conf)

        return self.data_lockers.get(method, locker_conf)
