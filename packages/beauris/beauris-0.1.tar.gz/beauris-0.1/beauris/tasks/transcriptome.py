import logging

from ..task import Task, TaskOutput

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class TranscriptomeTasks():

    entity_name = 'transcriptome'

    @staticmethod
    def get_tasks():

        return {
            'blastdb_transcriptome': BlastTranscriptomeTask,
        }


class BlastTranscriptomeTask(Task):

    params = {
        'specs_id': 'blastdb'
    }

    blastdb_exts = ['nhr', 'nin', 'nog', 'nsd', 'nsi', 'nsq']

    def get_derived_outputs(self, entity):

        outputs = []

        tool_version = '2.6.0'

        deps = [entity.input_files['fasta']]

        for ext in self.blastdb_exts:
            outputs.append(TaskOutput(name="blastdb_{}".format(ext), ftype=ext, path="transcriptome.{}".format(ext), tool_version=tool_version, publish=False, depends_on=deps))

        return outputs
