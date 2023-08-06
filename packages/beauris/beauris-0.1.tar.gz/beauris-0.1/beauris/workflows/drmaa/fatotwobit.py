#!/usr/bin/env python

import argparse
import logging
import os
import sys

from beauris import Beauris


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def main():
    """
    Generate a 2bit index from a fasta file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    task_id = "fatotwobit"

    exit_code_all = 0

    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{}.sh'.format(task_id))

    for ass in org.assemblies:
        genome_file = ass.get_input_path('fasta')
        output_file = ass.get_derived_path('2bit')
        options = ass.get_task_options(task_id)

        cmd_options = []

        for key, value in options:
            # fatotwobit only has bool parameters
            if value:
                cmd_options.append("-{}".format(options))

        job_args = [genome_file, output_file]

        if cmd_options:
            job_args.append(" ".join(cmd_options))

        runner = bo.get_runner('drmaa', ass, task_id)
        exit_code, stdout, stderr = runner.run_or_resume_job(script_path=script_path, job_args=job_args)

        exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))


if __name__ == '__main__':
    main()
