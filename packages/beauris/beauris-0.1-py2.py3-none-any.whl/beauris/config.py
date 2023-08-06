import logging
import os

from envsubst import envsubst

import yaml

from .tasks import Tasks


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Config():

    def __init__(self, root_work_dir=None, config_file=None):

        self.root_work_dir = root_work_dir if root_work_dir else os.getenv("WORK_DIR", None)

        if not self.root_work_dir:
            raise RuntimeError("Please specify a work dir (root_work_dir argument, or WORK_DIR environment variable)")

        self.known_tasks = Tasks()

        self.load_config(config_file)

    def load_config(self, config_file=None):

        # TODO document+validate this global config file
        config_file_path = config_file if config_file else "beauris.yml"

        if not os.path.isfile(config_file_path):
            raise RuntimeError("Could not find {}".format(config_file_path))

        with open(config_file_path, "r") as f:

            # Replace env vars in config file
            # TODO document this
            config_txt = envsubst(f.read())
            try:
                self.raw = yaml.safe_load(config_txt)
            except yaml.YAMLError:
                log.error("Invalid Beauris config yaml file : {}".format(config_file_path))
                raise

        self.job_specs = self.raw['job_specs'] if 'job_specs' in self.raw else {}

        self.deploy = {}
        if 'deploy' in self.raw and 'servers' in self.raw['deploy']:
            self.deploy = self.raw['deploy']['servers']

        self.deploy_services = {server: self.get_deploy_services(server) for server in self.get_deploy_servers()}

        self.tasks_by_entity = {}
        if 'tasks' in self.raw:
            for ent in self.raw['tasks']:
                if not self.known_tasks.has(ent):
                    raise RuntimeError("Unknown entity type in tasks configuration: {}".format(ent))

                if ent not in self.tasks_by_entity:
                    self.tasks_by_entity[ent] = {}

                ent_tasks = self.known_tasks.get(ent)

                if not self.raw['tasks'][ent]:
                    continue

                for taskid in self.raw['tasks'][ent]:
                    if taskid not in ent_tasks:
                        raise RuntimeError("Unknown task id '{}' for entity '{}' in tasks configuration".format(taskid, ent))

                    self.tasks_by_entity[ent][taskid] = ent_tasks[taskid]

    def get_deploy_servers(self):

        return self.deploy.keys()

    def get_deploy_services(self, server):

        if server in self.deploy:
            if 'services' in self.deploy[server]:
                return self.deploy[server]['services']

        return []

    def get_tasks(self, entity):
        # Give instanciated task objects for the given entity

        taskso = {}
        if entity.entity_name in self.tasks_by_entity:
            for tid, tc in self.tasks_by_entity[entity.entity_name].items():

                params = {}
                if hasattr(tc, 'params'):
                    params = tc.params
                new_task = tc(entity, tid, **params)

                if entity.accept_task(new_task):
                    taskso[tid] = new_task

        return taskso

    def get_service_url(self, service, server, organism=None):

        url = ''

        if service == 'apollo':
            url = self.raw['apollo'][server]["external_url"]
        else:
            if organism is None:
                raise RuntimeError("The 'organism' param is mandatory to get the url of service '{}'".format(service))

            base_url = self.deploy[server]["base_url"].rstrip("/")
            url_prefix = self.deploy[server]["url_prefix"].rstrip("/")

            url = '{}{}/{}/{}/'.format(base_url, url_prefix, organism.slug(), service)

        if not url.endswith('/'):
            url += '/'

        return url
