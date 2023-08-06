import logging

from ..task import Task, TaskOutput

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class ProteomeTasks():

    entity_name = 'proteome'

    @staticmethod
    def get_tasks():

        return {
            'blastdb_proteome': BlastProteomeTask,
        }


class BlastProteomeTask(Task):

    params = {
        'specs_id': 'blastdb'
    }

    blastdb_exts = ['phr', 'pin', 'pog', 'psd', 'psi', 'psq']

    def get_derived_outputs(self, entity):

        outputs = []

        tool_version = '2.6.0'

        deps = [entity.input_files['fasta']]

        for ext in self.blastdb_exts:
            outputs.append(TaskOutput(name="blastdb_{}".format(ext), ftype=ext, path="proteome.{}".format(ext), tool_version=tool_version, publish=False, depends_on=deps))

        return outputs
