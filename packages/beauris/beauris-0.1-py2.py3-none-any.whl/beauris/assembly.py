import logging
import os

from .annotation import Annotation
from .blastbank import BlastBank
from .managed_entity import ManagedEntity
from .managed_file import InputFile
from .track import Track


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Assembly(ManagedEntity):

    def __init__(self, config, yml_data, organism):

        ManagedEntity.__init__(self, config, default_services=organism.deploy_services, yml_data=yml_data)

        self.organism = organism

        self.version = self.yml_data['version']

        self.entity_name = 'assembly'

        # TODO this should be configurable somehow
        self.wig_category_suffix = " Coverage"

        self.input_files = {
            'fasta': InputFile.from_yml(self.yml_data["file"], name='fasta', version=self.version)
        }

        self.annotations = self._load_annotations()
        self.tracks = self._load_tracks()

        self.tasks = self.config.get_tasks(self)

        self.load_tasks_derived_files()

        self.blastbanks = [
            BlastBank(self, 'blastdb_assembly', self.input_files['fasta'], self.derived_files['blastdb_nhr'], "assembly", 'nucl')
        ]

    def get_blast_link(self, bank, server):

        link = '{id}'
        if 'jbrowse' in self.get_deploy_services(server):
            link = '<a href="' + self.config.get_service_url('jbrowse', server, self.organism) + '?data=data%2F' + self.slug(short=True) + '&loc={id}{jbrowse_track}">{id}</a>'

        if 'apollo' in self.get_deploy_services(server) and 'apollo' in self.config.raw and server in self.config.raw['apollo']:

            common_name = self.organism.pretty_name()
            common_name += " {}".format(self.version)
            common_name = common_name.replace(' ', '%20')

            link += ' <a href="{}annotator/loadLink?organism='.format(self.config.get_service_url('apollo', server)) + common_name + '&loc={id}{apollo_track}">Apollo</a>'

        return link

    def get_children(self):

        return self.annotations + self.tracks

    def get_organism(self):

        return self.organism

    def get_annotation(self, version):

        for annot in self.annotations:
            if annot.version == version:
                return annot

        return None

    def get_track(self, name):

        for tr in self.tracks:
            if tr.name == name:
                return tr

        return None

    def slug(self, short=False):

        if short:
            return "{}_ass{}".format(self.organism.slug(short), self.version)
        else:
            return "{}/assembly_{}".format(self.organism.slug(short), self.version)

    def pretty_name(self):

        return "{} assembly {}".format(self.organism.pretty_name(), self.version)

    def _load_annotations(self):
        annotations = []
        for annot in self.yml_data.get("annotations", []):
            annotations.append(Annotation(self.config, annot, self))

        return annotations

    def _load_tracks(self):
        tracks = []
        for track in self.yml_data.get("tracks", []):
            tracks.append(Track(self.config, track, self))

        return tracks

    def get_work_dir(self):

        return os.path.join(self.organism.get_work_dir(), "assembly_{}".format(self.version))

    def get_locked_yml(self):

        locked_yml = self.yml_data

        locked_yml['file'] = self.input_files['fasta'].to_yml()

        if len(self.derived_files):
            locked_yml['derived'] = []

            for id, der in self.derived_files.items():
                locked_yml['derived'].append(der.to_yml())

        if self.annotations:
            locked_yml['annotations'] = []

            for annot in self.annotations:
                locked_yml['annotations'].append(annot.get_locked_yml())

        if self.tracks:
            locked_yml['tracks'] = []

            for track in self.tracks:
                locked_yml['tracks'].append(track.get_locked_yml())

        return locked_yml

    def get_metadata(self):

        return self.organism.get_metadata() | {'assembly_version': self.version}

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)

        if 'file' in locked_yml:
            self.input_files['fasta'].merge_with_locked(locked_yml['file'], future)

        for annot in self.annotations:
            matching = annot.find_matching_yml_in_list(locked_yml.get("annotations", []))
            if matching:
                annot.load_locked_data(matching, future)

        for track in self.tracks:
            matching = track.find_matching_yml_in_list(locked_yml.get("tracks", []))
            if matching:
                track.load_locked_data(matching, future)

    def get_track_paths(self, prefer=None):

        tracks_paths = {}

        if prefer == 'locked':
            tracks_paths['gff'] = {(t.category, t.name): t.input_files['track_file'].get_locked_path() for t in self.tracks if t.type == "gff"}
            tracks_paths['bam'] = {(t.category, t.name): t.input_files['track_file'].get_locked_path() for t in self.tracks if t.type == "rnaseq"}
            tracks_paths['bai'] = {(t.category, t.name): t.derived_files['bai'].get_locked_path() for t in self.tracks if 'bai' in t.derived_files}
            tracks_paths['wig'] = {(t.category + self.wig_category_suffix, t.name): t.derived_files['wig'].get_locked_path() for t in self.tracks if 'wig' in t.derived_files}
        else:
            force_work_dir = prefer == 'workdir'

            tracks_paths['gff'] = {(t.category, t.name): t.get_input_path('track_file') for t in self.tracks if t.type == "gff"}
            tracks_paths['bam'] = {(t.category, t.name): t.get_input_path('track_file') for t in self.tracks if t.type == "rnaseq"}
            tracks_paths['bai'] = {(t.category, t.name): t.derived_files['bai'].get_usable_path(force_work_dir=force_work_dir or t.derived_files['bai'].task.needs_to_run()) for t in self.tracks if 'bai' in t.derived_files}
            tracks_paths['wig'] = {(t.category + self.wig_category_suffix, t.name): t.derived_files['wig'].get_usable_path(force_work_dir=force_work_dir or t.derived_files['wig'].task.needs_to_run()) for t in self.tracks if 'wig' in t.derived_files}

        return tracks_paths

    def jbrowse_track_swapping(self, json_tracks, tracks_real_path):

        to_swap = {}

        for jt in json_tracks:
            if 'storeClass' in jt and jt['storeClass'] == "JBrowse/Store/SeqFeature/BAM" and 'urlTemplate' in jt and (jt['category'], jt['key']) in tracks_real_path['bam']:
                to_swap[jt['urlTemplate']] = tracks_real_path['bam'][(jt['category'], jt['key'])]
                to_swap[jt['urlTemplate'] + ".bai"] = tracks_real_path['bai'][(jt['category'], jt['key'])]
            elif 'storeClass' in jt and jt['storeClass'] == "JBrowse/Store/SeqFeature/BigWig" and 'urlTemplate' in jt and (jt['category'], jt['key']) in tracks_real_path['wig']:
                to_swap[jt['urlTemplate']] = tracks_real_path['wig'][(jt['category'], jt['key'])]

        return to_swap
