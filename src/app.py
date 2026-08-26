import logging
from datetime import date, timedelta
from pathlib import Path
from sys import stdout

from .db import Database
from .repositories import FileRepository, ProjectRepository, TaskTagRepository
from .services import FileService, ProjectService, TaskTagService
from .ui import Interface


class App:
    '''Корневой класс приложения.'''

    def __init__(self, is_debug: bool):
        self._setup_logger(is_debug)
        self._clean_old_logs(days=7)

        self._logger = logging.getLogger('App')
        self._logger.info('Запус клиента...')

        self._db = Database()
        self._engine = self._db.engine

        self._project_repo = ProjectRepository(self._engine)
        self._file_repo = FileRepository(self._engine)
        self._task_tag_repo = TaskTagRepository(self._engine)

        self._file_service = FileService(self._file_repo, Path('assets/'))
        self._project_service = ProjectService(
            self._project_repo,
            self._file_service
        )
        self._task_tag_service = TaskTagService(self._task_tag_repo)

        self._interface = Interface(
            self._project_service,
            self._file_service,
            self._task_tag_service
        )

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

    def _clean_old_logs(self, days: int = 7):
        '''Удаление логов старше указанного количества дней.'''

        logs_dir = Path('logs/')
        if not logs_dir.exists():
            return

        cutoff_date = date.today() - timedelta(days=days)  # noqa: DTZ011
        for log_file in logs_dir.glob('*.log'):
            try:
                file_date_str = log_file.stem
                file_date = date.fromisoformat(file_date_str)
                if file_date < cutoff_date:
                    log_file.unlink()
                    self._logger.info(f'Удалён старый лог: {log_file.name}')
            except (ValueError, OSError):
                continue
