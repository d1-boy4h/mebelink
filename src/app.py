import logging
from datetime import date
from pathlib import Path

from .db import Database
from .repositories import ProjectRepository
from .services import ProjectService
from .ui import Interface

class App:
    '''Корневой класс приложения.'''

    def __init__(self):
        self._logger = logging.getLogger('App')

        self._db = Database()
        self._engine = self._db.engine

        self._project_repo = ProjectRepository(self._engine)
        self._project_service = ProjectService(self._project_repo)

        self._interface = Interface(self._project_service)

    def run(self):
        Path('logs/').mkdir(exist_ok=True)
        logging.basicConfig(
            filename=f'logs/{date.today()}.log',
            format='%(asctime)s [%(levelname)s | %(name)s] %(message)s',
            level=logging.INFO
        )

        self._logger.info('Запус клиента...')
        self._main()
        self._logger.info('Клиент завершил свою работу')

    def _main(self):
        self._interface.run()
