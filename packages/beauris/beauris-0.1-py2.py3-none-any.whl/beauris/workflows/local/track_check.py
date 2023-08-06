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
    task_id = "track_check"

    script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    exit_code_all = 0

    for ass in org.assemblies:
        for track in ass.tracks:

            log.info("Running track checker for {}".format(track.get_input_path('track_file')))

            runner = bo.get_runner('local', track, task_id)

            deps = [track.input_files['track_file']]
            runner.task.depends_on = deps

            # Run in a subprocess to capture stdout/stderr + exit code
            cmd = ["python", "{}/track_check_{}.py".format(script_dir, track.input_files['track_file'].type), track.get_input_path('track_file'), ass.get_input_path('fasta')]
            exit_code, out, err = runner.run_or_resume_job(cmd=cmd)

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
