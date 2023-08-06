import logging
import os

from .blastbank import BlastBank
from .managed_entity import ManagedEntity
from .managed_file import InputFile


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Proteome(ManagedEntity):

    def __init__(self, config, yml_data, organism):

        ManagedEntity.__init__(self, config, default_services=organism.deploy_services, yml_data=yml_data)

        self.organism = organism

        self.version = self.yml_data['version']

        self.entity_name = 'proteome'

        self.input_files = {
            'fasta': InputFile.from_yml(self.yml_data["file"], name='fasta', version=self.version)
        }

        self.tasks = self.config.get_tasks(self)

        self.load_tasks_derived_files()

        self.blastbanks = [
            BlastBank(self, 'blastdb_proteome', self.input_files['fasta'], self.derived_files['blastdb_phr'], "proteome", 'prot')
        ]

    def get_children(self):

        return []

    def get_organism(self):

        return self.organism

    def slug(self, short=False):

        if short:
            return "{}_prot{}".format(self.organism.slug(short), self.version)
        else:
            return "{}/proteome_{}".format(self.organism.slug(short), self.version)

    def pretty_name(self):

        return "{} proteome {}".format(self.organism.pretty_name(), self.version)

    def get_work_dir(self):

        return os.path.join(self.organism.get_work_dir(), "proteome_{}".format(self.version))

    def get_locked_yml(self):

        locked_yml = self.yml_data

        locked_yml['file'] = self.input_files['fasta'].to_yml()

        if len(self.derived_files):
            locked_yml['derived'] = []

            for id, der in self.derived_files.items():
                locked_yml['derived'].append(der.to_yml())

        return locked_yml

    def get_metadata(self):

        return self.organism.get_metadata() | {'proteome_version': self.version}

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)

        if 'file' in locked_yml:
            self.input_files['fasta'].merge_with_locked(locked_yml['file'], future)
