#!/usr/bin/env python

# Check that a genome fasta file is ready for release

import argparse
import logging
import re

from Bio import SeqIO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    log.info("Checking fasta {}".format(args.infile))

    pattern = re.compile("^[A-Za-z0-9-_.]+$")

    for record in SeqIO.parse(args.infile, "fasta"):
        if not pattern.match(record.id):
            raise RuntimeError("Invalid fasta header: {}".format(record.id))
