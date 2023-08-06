import hashlib
import logging
import os

import gitlab


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_state(file_path, hash=False):
    """
    Return a dict describing the current state of a file (to later check if it changed)
    """

    # Make sure we get stats from the real file if we look at a symlink
    real_path = os.path.realpath(file_path)

    file_stats = os.stat(real_path)

    state = {}

    state['size'] = file_stats.st_size
    state['last_modification'] = file_stats.st_mtime

    if hash:
        state['md5'] = md5(real_path)

    return state


def show_logs(out, err):
    log.info("-------------- STDOUT --------------")
    log.info(out)
    log.info("-------------- STDERR --------------")
    log.info(err)
    log.info("------------------------------------")


def find_mr_labels():

    labels = ""

    needed_env_vars = [
        'CI_PROJECT_ID',
        'CI_SERVER_URL',
        'GITLAB_BOT_TOKEN',
        'CI_COMMIT_BRANCH',
        'CI_DEFAULT_BRANCH',
    ]

    if 'CI_MERGE_REQUEST_LABELS' in os.environ:
        labels = os.getenv('CI_MERGE_REQUEST_LABELS', default="")
    elif all(item in os.environ for item in needed_env_vars) and os.getenv('CI_COMMIT_BRANCH') == os.getenv('CI_DEFAULT_BRANCH'):
        # Not in a merge request, but maybe this commit comes from a merged one on default branch

        gl_url = os.getenv('CI_SERVER_URL')
        gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))

        project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)
        commit = project.commits.get(os.getenv('CI_COMMIT_SHORT_SHA'))
        mrs = commit.merge_requests()

        if len(mrs) == 1 and 'labels' in mrs[0]:
            labels = mrs[0]['labels']

    if isinstance(labels, str):
        labels = labels.split(',')

    # log.info("Merge request labels: {}".format(labels))

    return labels


class Util():

    mr_labels = find_mr_labels()
