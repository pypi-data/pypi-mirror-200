#!/usr/bin/env python

import argparse
import logging
import os
import sys

from beauris import Beauris


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def run_blastdb(bo, bank):

    args_list = [bank.get_input_fasta_path(), bank.seq_type, bank.get_dest_path(), bank.title]
    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{}.sh'.format("blastdb"))

    runner = bo.get_runner('drmaa', bank.entity, bank.task_id)
    return runner.run_or_resume_job(script_path=script_path, job_args=args_list)


def main():
    """
    Generate blastdb banks
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    exit_code_all = 0
    all_banks = []

    for ass in org.assemblies:
        all_banks += ass.blastbanks

        for annot in ass.annotations:
            all_banks += annot.blastbanks

    for trans in org.transcriptomes:
        all_banks += trans.blastbanks

    for prot in org.proteomes:
        all_banks += prot.blastbanks

    if not all_banks:
        log.info("No fasta files found.")
    else:
        for bank in all_banks:
            exit_code, stdout, stderr = run_blastdb(bo, bank)
            exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some blastdb job failed for {}, see log above.'.format(org.slug()))
    else:
        log.info('All blastdb jobs succeeded for {}.'.format(org.slug()))

    sys.exit(exit_code_all)


if __name__ == '__main__':
    main()
