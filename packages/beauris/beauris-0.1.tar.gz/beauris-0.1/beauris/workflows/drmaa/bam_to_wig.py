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
    task_id = "bam_to_wig"

    script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    script_path = "{}/bam_to_wig.sh".format(script_dir)

    exit_code_all = 0

    for ass in org.assemblies:
        for track in ass.tracks:

            if 'bam_to_wig' in track.index_tasks():

                log.info("Converting bam to bigwig for {}".format(track.get_input_path('track_file')))

                runner = bo.get_runner('drmaa', track, task_id)

                # Run in a subprocess to capture stdout/stderr + exit code
                job_args = [track.get_input_path('track_file'), track.get_derived_path('bai'), ass.get_input_path('fasta'), track.get_derived_path('wig')]
                exit_code, out, err = runner.run_or_resume_job(script_path=script_path, job_args=job_args)

                if exit_code == 0:
                    log.info("Success ✅")
                else:
                    log.info("Failure ❌")

                exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
