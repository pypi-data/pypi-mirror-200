#!/usr/bin/env python

import argparse
import logging
import os
import sys

from pykwalify.core import Core

import yaml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="Organism yml file")

    args = parser.parse_args()

    errors = 0

    schema_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../validation/template')
    c = Core(source_file=args.infile, schema_files=[os.path.join(schema_path, 'schema.yaml')], extensions=[os.path.join(schema_path, 'ext.py')])
    c.validate(raise_exception=True)

    with open(args.infile, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError:
            log.error("Invalid Beauris config yaml file : {}".format(args.infile))
            raise

    if 'assemblies' in data:
        ass_versions = []
        for ass in data['assemblies']:
            if ass['version'] in ass_versions:
                log.error("Found a duplicate assembly version: {}".format(ass['version']))
                errors += 1
            ass_versions.append(ass['version'])

            if 'annotations' in ass:
                annot_versions = []
                for annot in ass['annotations']:
                    if annot['version'] in annot_versions:
                        log.error("Found a duplicate annotation version for assembly {}: {}".format(ass['version'], annot['version']))
                        errors += 1
                    annot_versions.append(annot['version'])

            if 'tracks' in ass:
                track_names = []
                for track in ass['tracks']:
                    if track['name'] in track_names:
                        log.error("Found a duplicate track name for assembly {}: {}".format(ass['version'], track['name']))
                        errors += 1
                    track_names.append(track['name'])

    if errors > 0:
        log.error("There were some errors in the {} organism config file".format(args.infile))
        sys.exit(1)
