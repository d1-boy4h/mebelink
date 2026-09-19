from pydantic import BaseModel

from .file import File
from .note import Note
from .project import Project
from .task import Task
from .task_tag import TaskTag


class Data(BaseModel):
    '''Pydantic-модель данных mblp-файла.'''

    project: Project
    files: list[File]
    task_tags: list[TaskTag]
    tasks: list[Task]
    notes: list[Note]
