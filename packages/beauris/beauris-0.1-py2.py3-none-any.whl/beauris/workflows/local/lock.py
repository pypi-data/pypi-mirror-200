#!/usr/bin/env python

# Lock files
import argparse
import logging

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', type=str, help="Organism yml file")
    parser.add_argument('--dry-run', action='store_true', help="Do not really lock data, just print what it would do.")

    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    locker = bo.get_data_locker()

    org.lock(locker, recursive=True, dry_run=args.dry_run)

    org.save_locked_yml()
