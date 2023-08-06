#!/usr/bin/env python

import collections
import json
import logging
import os


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class BlastBank:

    def __init__(self, entity, task_id, input_fasta, dest, fasta_type, seq_type):

        self.entity = entity
        self.task_id = task_id
        self.input_fasta = input_fasta  # An InputFile object
        self.dest = dest  # A DerivedFile object
        self.seq_type = seq_type

        self.title = entity.slug(short=True)

        self.pretty_name = entity.pretty_name()

        if fasta_type.startswith("annotation"):

            if fasta_type == 'annotation_transcripts':
                annot_type = "transcripts"
            elif fasta_type == 'annotation_cds':
                annot_type = "CDS"
            elif fasta_type == 'annotation_proteins':
                annot_type = "proteins"

            self.title += "_{}".format(annot_type)
            self.pretty_name += " {}".format(annot_type)

        # Just a stupid/hacky string used for sorting bank list
        self.sort_key = 'a_' if fasta_type == "genome" else 'b_'
        self.sort_key += self.pretty_name

    def get_blast_link(self, server):

        return self.entity.get_blast_link(self, server)

    def get_input_fasta_path(self):
        # Resolve it as late as possible to make sure it takes into account locked path

        return self.input_fasta.get_usable_path(force_work_dir=self.input_fasta.needs_to_run())

    def get_dest_path(self):
        # Resolve it as late as possible to make sure it takes into account locked path

        return os.path.splitext(self.dest.get_usable_path(force_work_dir=self.dest.needs_to_run()))[0]


class BankWriter:

    def __init__(self, banks, base_path, server):

        self.banks = banks
        self.base_path = base_path
        self.server = server

        self.nuc_list = collections.OrderedDict()
        self.prot_list = collections.OrderedDict()
        self.banks.sort(key=lambda x: x.sort_key)
        for b in self.banks:
            pretty_name = b.pretty_name
            tries = 1
            if b.seq_type == 'nucl':
                while pretty_name in self.nuc_list.values() and tries < 50:
                    pretty_name = "{} ({})".format(b.pretty_name, tries)
                self.nuc_list[b.get_dest_path()] = pretty_name
            else:
                while pretty_name in self.prot_list.values() and tries < 50:
                    pretty_name = "{} ({})".format(b.pretty_name, tries)
                self.prot_list[b.get_dest_path()] = pretty_name

    def write_bank_yml(self):
        # Safety check
        os.makedirs(self.base_path, exist_ok=True)

        banks_file_path = os.path.join(self.base_path, 'banks.yml')
        log.info("Writing bank list in '%s'" % banks_file_path)
        nuc = "~"
        prot = "~"

        if self.nuc_list:
            nuc = "\n                ".join(['%s: %s' % (json.dumps(k), json.dumps(v)) for k, v in self.nuc_list.items()])
        if self.prot_list:
            prot = "\n                ".join(['%s: %s' % (json.dumps(k), json.dumps(v)) for k, v in self.prot_list.items()])

        with open(banks_file_path, "w") as f:
            print("genouest_blast:", file=f)
            print("    db_provider:", file=f)
            print("        list:", file=f)
            print("            nucleic:", file=f)
            print("                %s" % nuc, file=f)
            print("            proteic:", file=f)
            print("                %s" % prot, file=f)

    def write_links_yml(self):
        # Safety check
        os.makedirs(self.base_path, exist_ok=True)

        links_file_path = os.path.join(self.base_path, 'links.yml')
        log.info("Writing automatic links to links.yml in '%s'" % links_file_path)

        with open(links_file_path, "w") as f:

            for bank in self.banks:
                print("", file=f)
                print("# %s" % (bank.pretty_name), file=f)

                link = bank.get_blast_link(self.server)

                if link:
                    print("%s:" % (bank.title), file=f)
                    print("    db: '^%s$'" % (bank.title), file=f)
                    print("    '*': '%s'" % (link), file=f)
                else:
                    print("# Skipped", file=f)


def prettify(name, capital=True):

    # A bit of magic to make even prettier names
    name = name.replace(" annot ogs", " ogs")
    name = name.replace("ogs", "OGS")

    return name


def sanitize(name):
    name = name.lower()
    name = name.replace(' ', '_')
    name = name.replace('/', '_')

    return name
