from ..models import File, Note, Project, TaskTag


class Store:
    '''Хранилище данных между экранами.'''

    def __init__(self) -> None:
        self.current_project: Project | None = None
        self.current_files: list[File] | None = None
        self.current_tags: list[TaskTag] | None = None
        self.current_notes: list[Note] | None = None

store = Store()
