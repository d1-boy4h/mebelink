from ..models import File, Project


class Store:
    '''Хранилище данных между экранами.'''

    def __init__(self) -> None:
        self.current_project: Project | None = None
        self.current_files: list[File] | None = None
        self.gallery_is_open: bool = False

store = Store()
