import logging

from ..task import Task

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class OrganismTasks():

    entity_name = 'organism'

    @staticmethod
    def get_tasks():

        return {
            'deploy_perms': DeployPermsTask,
            'deploy_download': DeployDownloadTask,
            'deploy_blast': DeployBlastTask,
            'deploy_jbrowse': DeployJBrowseTask,
        }


class DeployPermsTask(Task):

    params = {
        'always_run': True
    }


class DeployDownloadTask(Task):

    params = {
        'always_run': True
    }


class DeployBlastTask(Task):

    params = {
        'always_run': True
    }


class DeployJBrowseTask(Task):

    params = {
        'always_run': True
    }
