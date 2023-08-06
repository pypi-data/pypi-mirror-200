import logging
import os

import gitlab

import yaml

from .assembly import Assembly
from .managed_entity import ManagedEntity
from .proteome import Proteome
from .transcriptome import Transcriptome


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Organism(ManagedEntity):

    def __init__(self, config, yml_path, test_data=False, locked_dir=None, future_locked_dir=None, default_services=[]):

        ManagedEntity.__init__(self, config, yml_path=yml_path, locked_dir=locked_dir, future_locked_dir=future_locked_dir, default_services=default_services)

        self.yml_path = yml_path

        self.entity_name = 'organism'

        self.ci_prefix = None

        with open(yml_path, "r") as f:
            yml_str = f.read()
            if test_data:
                # This is a trick to ease tests
                yml_str = yml_str.replace('$TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../test-data')))
            try:
                self.yml_data = yaml.safe_load(yml_str)
            except yaml.YAMLError:
                log.error("Invalid organism yaml file : {}".format(yml_path))
                raise

        if 'computer_name' in self.yml_data:
            self.computer_name = self.yml_data['computer_name']
            self.computer_name_short = self.yml_data['computer_name']
        else:
            # TODO better computer_name guessing with strains
            self.computer_name = "{}_{}".format(self.yml_data['genus'], self.yml_data['species']).lower()
            self.computer_name_short = "{}{}".format(self.yml_data['genus'][:1], self.yml_data['species']).lower()
            if 'strain' in self.yml_data:
                self.computer_name = "{}_{}".format(self.computer_name, self.yml_data['strain']).lower()
            if 'sex' in self.yml_data and self.yml_data['sex'] != 'unknown':
                self.computer_name = "{}_{}".format(self.computer_name, self.yml_data['sex']).lower()

        self.genus = self.yml_data['genus']
        self.species = self.yml_data['species']
        self.strain = self.yml_data.get('strain', '')
        self.sex = self.yml_data.get('sex', '')

        self.task_options = self.load_task_options(self.yml_data)
        self.parse_services(self.yml_data)

        self.tasks = self.config.get_tasks(self)

        self.load_tasks_derived_files()

        self.restricted_to = self.yml_data.get('restricted_to', '')
        self.locked_restricted_to = ""

        self.assemblies = self._load_assemblies()

        self.transcriptomes = self._load_transcriptomes()

        self.proteomes = self._load_proteomes()

        self.load_locked_yml(test_data)

        self.load_locked_yml(test_data, future=True)

    def get_children(self):

        return self.assemblies + self.transcriptomes + self.proteomes

    def get_organism(self):

        return self

    def get_assembly(self, version):

        for ass in self.assemblies:
            if ass.version == version:
                return ass

        return None

    def slug(self, short=False):

        if short:
            return self.computer_name_short
        else:
            return self.computer_name

    def pretty_name(self):

        name_clean = "{} {}".format(self.genus, self.species).lower().capitalize()
        if self.strain:
            name_clean += " {}".format(self.strain)
        if self.sex:
            name_clean += " {}".format(self.sex)

        return name_clean

    def _load_assemblies(self):
        assemblies = []
        for ass in self.yml_data.get("assemblies", []):
            assemblies.append(Assembly(self.config, ass, self))

        return assemblies

    def _load_transcriptomes(self):
        transcriptomes = []
        for trans in self.yml_data.get("transcriptomes", []):
            transcriptomes.append(Transcriptome(self.config, trans, self))

        return transcriptomes

    def _load_proteomes(self):
        proteomes = []
        for trans in self.yml_data.get("proteomes", []):
            proteomes.append(Proteome(self.config, trans, self))

        return proteomes

    def get_ci_prefix(self):

        # Use cached value when possible
        if self.ci_prefix is not None:
            return self.ci_prefix

        needed_env_vars = [
            'CI_PROJECT_ID',
            'CI_SERVER_URL',
            'GITLAB_BOT_TOKEN',
            'CI_COMMIT_BRANCH',
            'CI_DEFAULT_BRANCH',
        ]

        prefix = ""

        if os.getenv('CI_MERGE_REQUEST_IID'):
            prefix = "{}-".format(os.getenv('CI_MERGE_REQUEST_IID'))
        elif all(item in os.environ for item in needed_env_vars) and os.getenv('CI_COMMIT_BRANCH') == os.getenv('CI_DEFAULT_BRANCH'):
            # Not in a merge request, but maybe this commit comes from a merged one on default branch

            gl_url = os.getenv('CI_SERVER_URL')
            gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))

            project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)
            commit = project.commits.get(os.getenv('CI_COMMIT_SHORT_SHA'))
            mrs = commit.merge_requests()

            if len(mrs) == 1 and 'iid' in mrs[0]:
                prefix = "{}-".format(mrs[0]['iid'])

        self.ci_prefix = prefix

        return prefix

    def get_work_dir(self, prefix=None):

        if prefix:
            dirname = prefix
        else:
            dirname = self.get_ci_prefix()

        dirname += self.computer_name

        return os.path.join(self.config.root_work_dir, dirname)

    def get_locked_yml(self):

        locked_yml = self.yml_data

        locked_yml['assemblies'] = []

        if self.assemblies:
            for ass in self.assemblies:
                locked_yml['assemblies'].append(ass.get_locked_yml())

        if self.transcriptomes:
            locked_yml['transcriptomes'] = []

            for trans in self.transcriptomes:
                locked_yml['transcriptomes'].append(trans.get_locked_yml())

        if self.proteomes:
            locked_yml['proteomes'] = []

            for trans in self.proteomes:
                locked_yml['proteomes'].append(trans.get_locked_yml())

        return locked_yml

    def get_metadata(self):

        return {
            'computer_name': self.computer_name,
            'genus': self.genus,
            'species': self.species,
            'strain': self.strain,
            'restricted_to': self.restricted_to,
        }

    def load_locked_yml(self, test_data=False, future=False):

        if future:
            ymlpath = self.future_locked_yml_path
        else:
            ymlpath = self.locked_yml_path

        if not os.path.isfile(ymlpath):
            log.info("No {}locked data found in '{}'".format("future " if future else "", ymlpath))
            return

        log.info("Loading locked data from {}".format(ymlpath))

        with open(ymlpath, "r") as f:
            yml_str = f.read()
            if test_data:
                # This is a trick to ease tests
                yml_str = yml_str.replace('$TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../test-data')))
            try:
                locked_yml_data = yaml.safe_load(yml_str)
            except yaml.YAMLError:
                log.error("Invalid {}locked yaml file : {}".format("future " if future else "", ymlpath))
                raise

        return self.load_locked_data(locked_yml_data, future)

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)
        self.locked_restricted_to = locked_yml.get("restricted_to", "")

        for ass in self.assemblies:
            ass.load_locked_data(ass.find_matching_yml_in_list(locked_yml.get("assemblies", [])), future)

        for trans in self.transcriptomes:
            trans.load_locked_data(trans.find_matching_yml_in_list(locked_yml.get("transcriptomes", [])), future)

        for trans in self.proteomes:
            trans.load_locked_data(trans.find_matching_yml_in_list(locked_yml.get("proteomes", [])), future)
