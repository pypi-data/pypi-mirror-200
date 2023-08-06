#!/usr/bin/env python

# Check that a bam file is ready for release

import argparse
import logging
import sys

from Bio import SeqIO

import pysam


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bamfile', type=str)
    parser.add_argument('genome', type=str)
    args = parser.parse_args()

    log.info("Checking bam {} against genome {}".format(args.bamfile, args.genome))
    log.info("(You can ignore the warning about missing index file)")

    fa_seqs = [r.id for r in SeqIO.parse(args.genome, "fasta")]

    bamfile = pysam.AlignmentFile(args.bamfile, "rb")
    bam_seqs = bamfile.references

    for bams in bam_seqs:
        if bams not in fa_seqs:
            log.error("Found unexpected scaffold '{}' in bam file".format(bams))
            sys.exit(1)

    # Check if bam file is sorted
    bam_stats_out = pysam.stats(args.bamfile)
    if "SN	is sorted:	0" in bam_stats_out:
        log.error("Bam file '{}' is unsorted".format(bams))
        sys.exit(1)
