#!/usr/bin/env python

import argparse
import logging
import os
import sys

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="Organism yml file")

    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)
    task_id = "fasta_check"

    script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../validation/ogs/"))

    exit_code_all = 0

    for ass in org.assemblies:

        log.info("Running fasta checker for {}".format(ass.get_input_path('fasta')))

        runner = bo.get_runner('local', ass, task_id)

        deps = [ass.input_files['fasta']]
        runner.task.depends_on = deps

        # Run in a subprocess to capture stdout/stderr + exit code
        cmd = ["python", "{}/fasta_check.py".format(script_dir), ass.get_input_path('fasta')]
        exit_code, out, err = runner.run_or_resume_job(cmd=cmd)

        exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
