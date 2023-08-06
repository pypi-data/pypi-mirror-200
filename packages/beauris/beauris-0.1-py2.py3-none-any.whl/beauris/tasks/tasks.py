import logging

from .annotation import AnnotationTasks
from .assembly import AssemblyTasks
from .organism import OrganismTasks
from .proteome import ProteomeTasks
from .track import TrackTasks
from .transcriptome import TranscriptomeTasks

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Tasks():
    def __init__(self):

        self.tasks = {}

        self.tasks[AnnotationTasks.entity_name] = AnnotationTasks.get_tasks()
        self.tasks[AssemblyTasks.entity_name] = AssemblyTasks.get_tasks()
        self.tasks[OrganismTasks.entity_name] = OrganismTasks.get_tasks()
        self.tasks[ProteomeTasks.entity_name] = ProteomeTasks.get_tasks()
        self.tasks[TrackTasks.entity_name] = TrackTasks.get_tasks()
        self.tasks[TranscriptomeTasks.entity_name] = TranscriptomeTasks.get_tasks()

    def has(self, entity_id):

        return entity_id in self.tasks

    def get(self, entity_id):

        if entity_id in self.tasks:
            return self.tasks[entity_id]

        raise RuntimeError('Could not find tasks for entity "%s"' % entity_id)
