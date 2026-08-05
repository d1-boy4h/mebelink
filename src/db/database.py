from sqlalchemy import create_engine

from .base import Base


class Database:
    '''Управление подключением к локальной SQLite.'''

    def __init__(self, path: str = 'data.db'):
        self.engine = create_engine(f'sqlite:///{path}')
        Base.metadata.create_all(self.engine)
