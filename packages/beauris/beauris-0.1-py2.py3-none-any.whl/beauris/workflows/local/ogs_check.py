#!/usr/bin/env python

# Check that an OGS GFF file is ready for release

import argparse
import filecmp
import logging
import os
import sys

from beauris import Beauris

import gitlab

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def report_changes(changed, unchanged):
    """
        Will report any changes to GFF files in the GitLab MR
    """

    if not changed and not unchanged:
        log.info("No GFF change to report")
        return

    needed_env_vars = [
        'CI_MERGE_REQUEST_IID',
        'CI_PROJECT_ID',
        'CI_SERVER_URL',
        'GITLAB_BOT_TOKEN',
        'CI_MERGE_REQUEST_PROJECT_URL'
    ]

    if not all(item in os.environ for item in needed_env_vars):
        log.info("Not in a GitLab MR or band env vars, can't report GFF changes")
        return

    gl_url = os.getenv('CI_SERVER_URL')
    log.info("Posting GFF change report to {}".format(gl_url))
    gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))

    project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)
    mr = project.mergerequests.get(os.getenv('CI_MERGE_REQUEST_IID'), lazy=True)

    note = """
The following GFF file(s) have been automatically checked, here's the report:

    """

    for chan in changed:
        note += "\n - 😕 `{}` was automatically modified:".format(chan.slug())
        note += "\n   - original file: `{}`".format(annot.get_input_path('gff'))
        note += "\n   - modified file: `{}`".format(annot.get_derived_path('fixed_gff'))

    for unchan in unchanged:
        note += "\n - ✅ `{}` did not require any modification".format(unchan.slug())
        note += "\n   - original file: `{}`".format(annot.get_input_path('gff'))
        note += "\n   - copied to: `{}`".format(annot.get_derived_path('fixed_gff'))

    # TODO make this url more configurable
    note += "\n\nIf you merge this MR now, the modified file(s) will be published. If you don't want that, modify the original file manually, or adapt the [automatic correction script]({}).".format("https://gitlab.com/beaur1s/beauris/-/blob/master/beauris/validation/ogs/ogs_check.py")

    mr.notes.create({'body': note})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="Organism yml file")
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    task_id = "ogs_check"
    script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../validation/ogs/"))

    exit_code_all = 0

    changed = []
    unchanged = []

    did_run = False

    for ass in org.assemblies:
        for annot in ass.annotations:

            log.info("Running gff checker for {}".format(annot.get_input_path('gff')))

            options = annot.get_task_options(task_id)
            cmd_options = []
            if 'adopt_rna_suffix' in options:
                if not options['adopt_rna_suffix']:
                    options['adopt_rna_suffix'] = ''
                cmd_options.append("--adopt-rna-suffix=%s" % options['adopt_rna_suffix'])
            if 'rna_prefix' in options and options['rna_prefix']:
                cmd_options.append("--rna-prefix=%s" % options['rna_prefix'])
            if 'source' in options and options['source']:
                cmd_options.append("--source")
                cmd_options.append(options['source'])
            if 'no_size' in options:
                cmd_options.append("--no-size")
            if 'exons_are_cds' in options:
                cmd_options.append("--exons-are-cds")

            # Run in a subprocess to capture stdout/stderr + exit code
            cmd = ["python",
                   "{}/ogs_check.py".format(script_dir)]
            cmd += cmd_options
            cmd += [annot.get_input_path('gff'),
                    ass.get_input_path('fasta'),
                    annot.get_derived_path('fixed_gff')]

            runner = bo.get_runner('local', annot, task_id)
            did_run = did_run or runner.task.needs_to_run()
            exit_code, out, err = runner.run_or_resume_job(cmd=cmd)

            exit_code_all += exit_code

            # Remember any change
            if os.path.exists(annot.get_derived_path('fixed_gff')):
                if not filecmp.cmp(annot.get_input_path('gff'), annot.get_derived_path('fixed_gff')):
                    changed.append(annot)
                else:
                    unchanged.append(annot)

    if did_run:
        report_changes(changed, unchanged)

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
