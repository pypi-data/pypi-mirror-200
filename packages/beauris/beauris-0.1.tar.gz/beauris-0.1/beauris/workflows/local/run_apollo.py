#!/usr/bin/env python

# Send an organism archive to a remote Apollo server

import argparse
import logging
import sys

from apollo import ApolloInstance

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def check_organism(wa, slug):
    return wa.organisms.show_organism(slug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true', help="Should the organism be updated?")
    parser.add_argument('infile', type=str, help="Jbrowse archive file")
    parser.add_argument('cname', type=str, help="Common name")
    parser.add_argument('genus', type=str, help="Genus")
    parser.add_argument('species', type=str, help="Species")
    parser.add_argument('url', type=str, help="Apollo server URL")
    parser.add_argument('user', type=str, help="Apollo server user")
    parser.add_argument('password', type=str, help="Apollo server password")
    args = parser.parse_args()

    wa = ApolloInstance(args.url, args.user, args.password)

    previous_org = check_organism(wa, args.cname)

    log.info(previous_org)

    if previous_org and 'error' not in previous_org:
        log.info('{} already exists in Apollo, with id {}'.format(args.cname, previous_org['id']))
        if args.update:
            res = wa.remote.update_organism(previous_org['id'], open(args.infile, 'rb'), genus=args.genus, species=args.species)
            if 'error' in res:
                log.error("Error while updating organism {}: {}".format(args.cname, res['error']))
                sys.exit(1)
        else:
            log.info("No --update parameter was passed, skipping.")

    else:
        log.info('{} not found yet in Apollo, creating a new organism'.format(args.cname))
        res = wa.remote.add_organism(args.cname, open(args.infile, 'rb'), genus=args.genus, species=args.species)
        if 'error' in res:
            log.error("Error while creating organism {}: {}".format(args.cname, res['error']))
            sys.exit(1)
        else:
            log.info('Created organism {}'.format(args.cname))

    # Raise an error if there were some logged
    if 40 in log._cache and log._cache[40]:
        sys.exit(1)
