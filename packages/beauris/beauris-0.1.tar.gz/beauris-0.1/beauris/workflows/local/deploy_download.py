#!/usr/bin/env python

import argparse
import logging
import sys


from beauris import Beauris
from beauris.web_interface import WebInterface

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()

    if not bo.config.raw['deploy']['deploy_interface']:
        log.info("Skipping docker setup")
        sys.exit(0)

    org = bo.load_organism(args.infile)

    web_interface = WebInterface(org, bo.config, args.server)

    deploy_download = 'download' in org.get_deploy_services(args.server)

    if deploy_download:
        log.info("Setting up download symlinks")
        web_interface.prepare_download()
    else:
        log.info("Skipping download setup")


if __name__ == '__main__':
    main()
