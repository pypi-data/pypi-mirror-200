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

    log.info("Setting up jbrowse")

    web_interface._create_jbrowse_data_dir()

    for ass in org.assemblies:
        runner = bo.get_runner('local', ass, 'deploy_jbrowse', args.server)

        deps = [ass.derived_files['jbrowse']]
        runner.task.depends_on = deps

        if runner.task.needs_to_run() and not runner.task.disable_run():
            web_interface.setup_jbrowse(ass)

    web_interface.write_jbrowse_datasets()


if __name__ == '__main__':
    main()
