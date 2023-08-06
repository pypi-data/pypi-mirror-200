#!/usr/bin/env python

# Set permissions on an organism on a remote Apollo server

import argparse
import logging
import os
import sys

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)
    task_id = "apollo_perms"

    script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./"))

    exit_code_all = 0

    if 'apollo' not in org.get_deploy_services(args.server):
        log.info('Skipping Apollo permissions update')
        sys.exit(0)

    if 'apollo' not in bo.config.raw or args.server not in bo.config.raw['apollo'] \
       or 'url' not in bo.config.raw['apollo'][args.server] \
       or 'user' not in bo.config.raw['apollo'][args.server] \
       or 'password' not in bo.config.raw['apollo'][args.server]:
        log.error('Invalid Apollo credentials for server {}.'.format(args.server))
        sys.exit(1)

    for ass in org.assemblies:

        common_name = ass.organism.pretty_name()
        common_name += " {}".format(ass.version)

        log.info("Updating permissions in Apollo for {}".format(common_name))

        # Manage permissions
        runner = bo.get_runner('local', ass, task_id)

        # Need to check previous run parameters
        previous_state = runner.task.load_previous_data_state()
        # If first run of this task, get the locked value
        previous_group = previous_state.get("restricted_to", "") if "restricted_to" in previous_state else org.locked_restricted_to
        current_group = org.restricted_to

        if not previous_group == current_group:
            cmd = ["python", "{}/run_apollo_perms.py".format(script_dir)]
            if previous_group:
                cmd += ["--previous={}".format(previous_group)]
            if current_group:
                cmd += ["--restricted={}".format(current_group)]
            cmd += [common_name, bo.config.raw['apollo'][args.server]['url'], bo.config.raw['apollo'][args.server]['user'], bo.config.raw['apollo'][args.server]['password']]
            # Force to run if anything has changed since last run (or lock, if no last run)
            exit_code, out, err = runner.run_or_resume_job(cmd=cmd, since='last_run')

            exit_code_all += exit_code
        else:
            log.info("No change in permissions for {}, skipping".format(ass.slug()))

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
