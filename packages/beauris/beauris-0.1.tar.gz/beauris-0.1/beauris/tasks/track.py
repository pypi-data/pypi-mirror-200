import logging

from ..task import Task, TaskOutput

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class TrackTasks():

    entity_name = 'track'

    @staticmethod
    def get_tasks():

        return {
            'track_check': TrackCheckTask,
            'index_bai': IndexBaiTask,
            'bam_to_wig': BamToWigTask,
        }


class TrackCheckTask(Task):

    pass


class IndexBaiTask(Task):

    def get_derived_outputs(self, entity):

        deps = [entity.input_files['track_file']]

        tool_version = '1.15'

        return [
            TaskOutput(name='bai', ftype='bai', path='index.bai', tool_version=tool_version, publish=False, depends_on=deps),
        ]


class BamToWigTask(Task):

    def get_derived_outputs(self, entity):

        deps = [entity.input_files['track_file']]

        tool_version = '3.4.2'

        return [
            TaskOutput(name='wig', ftype='wig', path='index.wig', tool_version=tool_version, publish=False, depends_on=deps),
        ]
