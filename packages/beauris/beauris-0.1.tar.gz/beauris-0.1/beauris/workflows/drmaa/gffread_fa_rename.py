#!/usr/bin/env python

import argparse
import logging
import re

from BCBio import GFF

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def replace_ids_in_fa(infile, outfile, ncbi, regex, replace, id_map):
    with open(infile, 'r') as infa, open(outfile, 'w') as outfa:
        for line in infa:
            if line.startswith(">"):

                if ncbi:
                    cur_id = line[1:].split(' ')[0].strip()

                    if cur_id in id_map:
                        line = ">{}".format(id_map[cur_id])
                else:
                    line = re.sub(regex, replace, line)

            outfa.write("%s\n" % line.strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--regex", help="Regex to parse input ids", default=r"([A-Za-z0-9]+)-R([A-Z]+( .*)?)")
    parser.add_argument("--replace", help="Replacement string", default=r"\1-P\2")
    parser.add_argument('--ncbi-ids', type=str, help="Name mrna/proteins after NCBI attributes in gff")
    parser.add_argument('prefix', type=str)
    args = parser.parse_args()

    ncbi_map_transcripts = {}
    ncbi_map_proteins = {}

    if args.ncbi_ids:

        log.info("Renaming sequences using attributes from an NCBI gff file")

        for scaff in GFF.parse(open(args.ncbi_ids, 'r')):

            for feat in scaff.features:
                if feat.type == 'gene':
                    for sf in feat.sub_features:
                        if sf.type == "mRNA" and 'ID' in sf.qualifiers:
                            mrna_raw_id = sf.qualifiers['ID'][0]

                            if 'transcript_id' in sf.qualifiers:
                                transcript_id = sf.qualifiers['transcript_id'][0]

                            protein_id = None
                            for ssf in sf.sub_features:
                                if ssf.type == 'CDS' and 'protein_id' in ssf.qualifiers:
                                    protein_id = ssf.qualifiers['protein_id'][0]
                                    break

                            if mrna_raw_id and transcript_id:
                                ncbi_map_transcripts[mrna_raw_id] = transcript_id
                            if mrna_raw_id and protein_id:
                                ncbi_map_proteins[mrna_raw_id] = protein_id
    else:
        log.info("Renaming sequences using regex: {} -> {}".format(args.regex, args.replace))

    cds_fa_in = "{}_cds_raw.fa".format(args.prefix)
    transcripts_fa_in = "{}_transcripts_raw.fa".format(args.prefix)
    proteins_fa_in = "{}_proteins_raw.fa".format(args.prefix)

    cds_fa_out = "{}_cds.fa".format(args.prefix)
    transcripts_fa_out = "{}_transcripts.fa".format(args.prefix)
    proteins_fa_out = "{}_proteins.fa".format(args.prefix)

    replace_ids_in_fa(cds_fa_in, cds_fa_out, ncbi=args.ncbi_ids, regex=args.regex, replace=args.replace, id_map=ncbi_map_transcripts)
    replace_ids_in_fa(transcripts_fa_in, transcripts_fa_out, ncbi=args.ncbi_ids, regex=args.regex, replace=args.replace, id_map=ncbi_map_transcripts)
    replace_ids_in_fa(proteins_fa_in, proteins_fa_out, ncbi=args.ncbi_ids, regex=args.regex, replace=args.replace, id_map=ncbi_map_proteins)
