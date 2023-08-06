import logging
import os
import re

from .managed_entity import ManagedEntity
from .managed_file import InputFile

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Track(ManagedEntity):

    def __init__(self, config, yml_data, assembly):

        ManagedEntity.__init__(self, config, default_services=assembly.deploy_services, yml_data=yml_data)

        self.assembly = assembly

        self.name = yml_data['name']
        self.safe_name = re.sub(r'[^a-zA-Z0-9-]', '_', self.name)
        self.type = yml_data['type']

        self.version = "0"  # No version for this kind of data

        self.entity_name = 'track'

        # Trick to have better looking names
        type_to_category = {
            'rnaseq': 'RNA-Seq'
        }

        if 'category' in yml_data:
            self.category = yml_data['category']
        elif self.type in type_to_category:
            self.category = type_to_category[self.type]
        else:
            self.category = self.type

        no_lock = self.type == 'rnaseq' and self.yml_data["file"]['type'] == 'bam'
        self.input_files = {
            'track_file': InputFile.from_yml(self.yml_data["file"], name='track_file', version=self.version, no_lock=no_lock)
        }

        self.tasks = self.config.get_tasks(self)

        self.load_tasks_derived_files()

    def slug(self, short=False):

        if short:
            return "{}_track{}".format(self.assembly.slug(short), self.safe_name)
        else:
            return "{}/track_{}".format(self.assembly.slug(short), self.safe_name)

    def pretty_name(self):

        return "{} track {}".format(self.assembly.pretty_name(), self.safe_name)

    def get_work_dir(self):

        return os.path.join(self.assembly.get_work_dir(), "track_{}".format(self.safe_name))

    def get_locked_yml(self):

        locked_yml = self.yml_data

        locked_yml['file'] = self.input_files['track_file'].to_yml()

        if len(self.derived_files):
            locked_yml['derived'] = []

            for id, der in self.derived_files.items():
                locked_yml['derived'].append(der.to_yml())

        return locked_yml

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)

        if 'file' in locked_yml:
            self.input_files['track_file'].merge_with_locked(locked_yml["file"], future)

    def get_metadata(self):

        return self.assembly.get_metadata() | {'track_id': '{}_{}'.format(self.safe_name, self.version)}

    def find_matching_yml_in_list(self, yml):
        """
        Find a yml subelement from a list matching the current object
        """

        for ysub in yml:
            if ysub["name"] == self.name:
                return ysub

        return {}

    def index_tasks(self):

        tasks = []

        if self.type == 'rnaseq' and self.yml_data["file"]['type'] == 'bam':
            tasks = ['index_bai', 'bam_to_wig']

        return tasks

    def accept_task(self, task):
        """
        Some entities can refuse to run selected tasks if not applicable
        """

        allowed_tasks = self.index_tasks() + ['track_check']
        return task.name in allowed_tasks
