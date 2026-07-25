from ..models import Project

class Store:
    '''Хранилище данных между экранами.'''

    def __init__(self):
        self.current_project: Project | None = None

store = Store()
