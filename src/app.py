import logging
from datetime import date
from pathlib import Path
from sys import stdout

from .db import Database
from .repositories import FileRepository, ProjectRepository
from .services import FileService
from .ui import Interface


class App:
    '''Корневой класс приложения.'''

    def __init__(self, is_debug: bool):
        self._setup_logger(is_debug)

        self._logger = logging.getLogger('App')
        self._logger.info('Запус клиента...')

        self._db = Database()
        self._engine = self._db.engine

        self._project_repo = ProjectRepository(self._engine)
        self._file_repo = FileRepository(self._engine)

        self._file_service = FileService(self._file_repo, Path('files/'))

        self._interface = Interface(self._project_repo)

    def run(self):
        '''Запуск приложения.'''

        self._interface.run()
        self._logger.info('Клиент завершил свою работу')

    def _setup_logger(self, is_debug: bool):
        '''Установка логирования.'''

        Path('logs/').mkdir(exist_ok=True)

        formatter_str = '%(asctime)s [%(levelname)s | %(name)s] %(message)s'
        formatter = logging.Formatter(formatter_str)

        file_handler = logging.FileHandler(
            f'logs/{date.today()}.log',  # noqa: DTZ011
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        handlers_list: list = [file_handler]
        if is_debug:
            console_handler = logging.StreamHandler(stdout)
            console_handler.setFormatter(formatter)
            handlers_list.append(console_handler)

        logging.basicConfig(
            level=logging.INFO,
            handlers=handlers_list
        )
