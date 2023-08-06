#!/usr/bin/env python

# Check that an OGS GFF file is ready for release

import argparse
import logging
import os
import re

from beauris import Beauris

import gitlab

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def reuse_previous_work_dir(org):

    new_work_dir = org.get_work_dir()

    needed_env_vars = [
        'CI_PROJECT_ID',
        'CI_SERVER_URL',
        'GITLAB_BOT_TOKEN',
        'CI_MERGE_REQUEST_IID',
    ]

    if all(item in os.environ for item in needed_env_vars):

        gl_url = os.getenv('CI_SERVER_URL')
        gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))

        project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)
        mr = project.mergerequests.get(os.getenv('CI_MERGE_REQUEST_IID'))

        if mr and mr.title:
            mr_title = mr.title.lower().strip()
            match = re.search('.* fu([0-9]+)', mr_title)
            if match:
                old_mr_id = match.group(1)
                log.info('This MR is a follow-up to MR !{}'.format(old_mr_id))
                old_mr = project.mergerequests.get(old_mr_id)
                if old_mr and old_mr.state:
                    if old_mr.state != 'merged':
                        raise RuntimeError("The follow-up MR !{} is not in 'merged' state, refusing to reuse it.".format(old_mr_id))

                    old_work_dir = org.get_work_dir("{}-".format(old_mr_id))

                    if not os.path.isdir(old_work_dir):
                        raise RuntimeError("The follow-up MR !{} does not have a valid work dir, refusing to reuse it.".format(old_mr_id))

                    if os.path.islink(new_work_dir):
                        if os.readlink(new_work_dir) == old_work_dir:
                            log.info("Work dir is already a symlink pointing to the one from MR !{}, no change".format(old_mr_id))
                        else:
                            raise RuntimeError("Work dir is a symlink not pointing to the expected target ('{}' instead of '{}'). Refusing to do anything.".format(os.readlink(new_work_dir), old_work_dir))
                    elif os.path.exists(new_work_dir):
                        raise RuntimeError("Work dir already exists, but not as a symlink. Refusing to do anything.")
                    else:
                        log.info("Creating work dir as a symlink pointing to the one from MR !{}".format(old_mr_id))
                        os.symlink(old_work_dir, new_work_dir)
                else:
                    raise RuntimeError("Could not find a valid follow-up MR !{}, remove/correct it in the MR title".format(old_mr_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)
    log.info("Creating organism workdir %s" % org.get_work_dir())
    reuse_previous_work_dir(org)
    org.create_work_dir()
