#!/usr/bin/env python

import argparse
import logging
import sys


from beauris import Beauris
from beauris.web_interface import WebInterface

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def run_deploy_task(task_id, org, job_args, bo, server):
    runner = bo.get_runner('local', org, task_id, server)
    cmd = ["python", "-m", "beauris.workflows.local." + task_id] + job_args
    exit_code, stdout, stderr = runner.run_or_resume_job(cmd=cmd)
    return exit_code


def main():
    """
    Setup deployment files
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()

    if not bo.config.raw['deploy']['deploy_interface']:
        log.info("Missing deployment params in beauris.yml, skipping docker setup")
        sys.exit(0)

    org = bo.load_organism(args.infile)

    log.info("Services to deploy: {}".format(org.get_deploy_services(args.server)))

    deploy_blast = 'blast' in org.get_deploy_services(args.server)
    deploy_download = 'download' in org.get_deploy_services(args.server)
    deploy_jbrowse = 'jbrowse' in org.get_deploy_services(args.server)
    deploy_perms = 'authelia' in org.get_deploy_services(args.server)

    exit_code_all = 0

    job_args = [args.server, args.infile]

    web_interface = WebInterface(org, bo.config, args.server)

    if args.server == "staging":
        log.info("Staging mode, shutting down running UIs")
        web_interface.shutdown()

    if not any([deploy_blast, deploy_download, deploy_jbrowse, deploy_perms]):
        log.info("No docker service to deploy.")
        sys.exit(0)

    if deploy_perms:
        exit_code_all += run_deploy_task("deploy_perms", org, job_args, bo, args.server)

    if deploy_download:
        exit_code_all += run_deploy_task("deploy_download", org, job_args, bo, args.server)

    if deploy_blast:
        exit_code_all += run_deploy_task("deploy_blast", org, job_args, bo, args.server)

    if deploy_jbrowse:
        exit_code_all += run_deploy_task("deploy_jbrowse", org, job_args, bo, args.server)

    log.info("Setting up interface files")
    web_interface.write_interface_files()

    log.info("Starting up application")
    web_interface.start()

    if exit_code_all != 0:
        log.error('Some interface setup job failed with exit code {} for {}, see log above.'.format(exit_code_all, org.slug()))
    else:
        log.info('All interface setup jobs succeeded for {}.'.format(org.slug()))

    sys.exit(min(exit_code_all, 255))


if __name__ == '__main__':
    main()
