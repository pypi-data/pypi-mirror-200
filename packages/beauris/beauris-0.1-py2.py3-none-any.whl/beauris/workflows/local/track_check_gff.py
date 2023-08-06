#!/usr/bin/env python

# Check that a bam file is ready for release

import argparse
import logging
import sys

from BCBio import GFF

from Bio import SeqIO


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gfffile', type=str)
    parser.add_argument('genome', type=str)
    args = parser.parse_args()

    log.info("Checking gff {} against genome {}".format(args.gfffile, args.genome))

    fa_seqs = [r.id for r in SeqIO.parse(args.genome, "fasta")]
    gff_seqs = [r.id for r in GFF.parse(args.gfffile)]

    for gffs in gff_seqs:
        if gffs not in fa_seqs:
            log.error("Found unexpected scaffold '{}' in gff file".format(gffs))
            sys.exit(1)

    # We could do more checks but
    #  1) we need to accept gff taht are not as standard as an OGS gff
    #  2) GFF.parse will detect obvious problems
