import logging

from ..task import Task, TaskOutput

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class AnnotationTasks():

    entity_name = 'annotation'

    @staticmethod
    def get_tasks():

        return {
            'ogs_check': OgsCheckTask,
            'gffread': GffReadTask,
            'func_annot_bipaa': FuncAnnotBipaaTask,
            'func_annot_orson': FuncAnnotOrsonTask,
            'blastdb_cds': BlastCdsTask,
            'blastdb_proteins': BlastProteinsTask,
            'blastdb_transcripts': BlastTranscriptsTask,
        }


class OgsCheckTask(Task):

    def get_derived_outputs(self, entity):

        deps = [entity.assembly.input_files['fasta'], entity.input_files['gff']]

        return [
            TaskOutput(name='fixed_gff', ftype='gff', path='fixed.gff', depends_on=deps),
        ]


class GffReadTask(Task):

    def get_derived_outputs(self, entity):

        deps = [entity.assembly.input_files['fasta'], entity.input_files['gff']]

        tool_version = '0.12.7'

        return [
            TaskOutput(name='cds_fa', ftype='fasta', path="{}_cds.fa".format(entity.slug(True)), tool_version=tool_version, depends_on=deps),
            TaskOutput(name='proteins_fa', ftype='fasta', path="{}_proteins.fa".format(entity.slug(True)), tool_version=tool_version, depends_on=deps),
            TaskOutput(name='transcripts_fa', ftype='fasta', path="{}_transcripts.fa".format(entity.slug(True)), tool_version=tool_version, depends_on=deps),
        ]


class FuncAnnotBipaaTask(Task):

    def get_derived_outputs(self, entity):

        deps = [entity.derived_files['proteins_fa']]

        return [
            TaskOutput(name='blast2go_annot', ftype='tsv', path="results/blast2go.annot", tool_version='2.5', depends_on=deps),
            TaskOutput(name='blast2go_gaf', ftype='tsv', path="results/blast2go.gaf", tool_version='2.5', depends_on=deps),
            TaskOutput(name='blast2go_pdf', ftype='pdf', path="results/blast2go_report.pdf", tool_version='2.5', depends_on=deps),
            TaskOutput(name='diamond', ftype='xml', path="results/diamond_all.xml", tool_version="2.0.13 on NR 2022-11-30", depends_on=deps),
            TaskOutput(name='eggnog', ftype='tsv', path="results/eggnog_annotations.tsv", tool_version="2.1.9", depends_on=deps),
            TaskOutput(name='interproscan', ftype='tsv', path="results/interproscan.tsv", tool_version='5.59-91.0', depends_on=deps),
            TaskOutput(name='func_annot_readme', ftype='txt', path="results/README", depends_on=deps),
        ]


class FuncAnnotOrsonTask(Task):

    dmnd_ext = ['tab', 'xml']
    iprscan_ext = ['tsv', 'xml']
    emap_ext = ['annotations', 'hits', 'seed_orthologs']

    def get_derived_outputs(self, entity):

        options = entity.get_task_options(self.name)
        deps = [entity.derived_files['proteins_fa']]
        outputs = []
        for ext in self.dmnd_ext:
            outputs.append(TaskOutput(name='diamond_{}'.format(ext), ftype=ext,
                           path="results/03_final_results/merged_diamond.{}".format(ext),
                           tool_version="2.0.15 on Uniref90 2022-03", depends_on=deps))
        for ext in self.emap_ext:
            outputs.append(TaskOutput(name='eggnog_{}'.format(ext), ftype=ext,
                           path="results/03_final_results/result.emapper.{}".format(ext),
                           tool_version="2.1.9", depends_on=deps))
        for ext in self.iprscan_ext:
            outputs.append(TaskOutput(name='interproscan_{}'.format(ext), ftype=ext,
                           path="results/03_final_results/merged_iprscan.{}".format(ext),
                           tool_version='5.59-91.0', depends_on=deps))
        if 'hectar' in options and options['hectar']:
            outputs.append(TaskOutput(name='hectar', ftype='csv',
                           path="results/03_final_results/result_hectar.csv",
                           tool_version="1.3", depends_on=deps))
        return outputs


class BlastTask(Task):

    blastdb_exts = ['nhr', 'nin', 'nog', 'nsd', 'nsi', 'nsq']

    fa_type = 'xxx'  # Adapt this in subclasses

    params = {
        'specs_id': 'blastdb'
    }

    def get_derived_outputs(self, entity):

        outputs = []

        tool_version = '2.6.0'

        deps = [entity.derived_files['proteins_fa'], entity.derived_files['cds_fa'], entity.derived_files['transcripts_fa']]

        fasta_file = [file for file in entity.derived_files.values() if file.type == "fasta"]

        for file in fasta_file:
            annot_type = file.name.split("_fa")[0]
            for ext in self.blastdb_exts:
                if self.fa_type in file.name:

                    outputs.append(TaskOutput(name="blastdb_{}_{}".format(annot_type, ext), ftype=ext, path="annotation_{}.{}".format(annot_type, ext), tool_version=tool_version, publish=False, depends_on=deps))

        return outputs


class BlastProteinsTask(BlastTask):

    blastdb_exts = ['phr', 'pin', 'pog', 'psd', 'psi', 'psq']

    fa_type = 'proteins'


class BlastCdsTask(BlastTask):

    fa_type = 'cds'


class BlastTranscriptsTask(BlastTask):

    fa_type = 'transcripts'
