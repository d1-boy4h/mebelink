import logging
import shutil
from pathlib import Path
from uuid import UUID

from ..models import File
from ..repositories import FileRepository


class FileService:
    '''Сервис работы с файлами проектов.'''

    def __init__(self, file_repo: FileRepository, storage_path: Path):
        self._file_repo = file_repo
        self._storage_path = storage_path
        self._logger = logging.getLogger('FileService')

    def _get_project_dir(self, project_uuid: UUID) -> Path:
        '''Получение пути к папке проекта.'''

        project_dir = self._storage_path / str(project_uuid)
        project_dir.mkdir(parents=True, exist_ok=True)

        return project_dir

    def save_file(self, project_uuid: UUID, name: str, content: bytes) -> File:
        '''Сохранение файла на диск и в БД.'''

        project_dir = self._get_project_dir(project_uuid)
        file_path = project_dir / name

        if file_path.exists():
            raise ValueError('Данный файл уже существует')

        file_path.write_bytes(content)

        return self._file_repo.save(File(
            project_uuid=project_uuid,
            filename=name,
            path=str(file_path)
        ))

    def get_all(self, project_uuid: UUID) -> list[File]:
        '''Получение всех файлов проекта.'''
        return self._file_repo.get_by_project(project_uuid)

    def delete_file(self, file: File) -> File | None:
        '''Удаление файла с диска и БД.'''

        file_path = Path(file.path)
        if file_path.exists():
            file_path.unlink()
            self._logger.info(f'Физический файл \'{file.filename}\' удалён')

            project_dir = self._get_project_dir(file.project_uuid)
            if project_dir.exists() and not any(Path(project_dir).iterdir()):
                project_dir.rmdir()

        return self._file_repo.delete(file)

    def delete_project_files(self, project_uuid: UUID) -> list[File]:
        '''Удаление всех файлов проекта.'''

        project_dir = self._get_project_dir(project_uuid)
        if project_dir.exists():
            shutil.rmtree(project_dir)
            self._logger.info(f'Папка проекта \'{project_uuid!s}\' удалена')

        files = self._file_repo.get_by_project(project_uuid)
        deleted_files = []
        for file in files:
            if file.id is not None:
                deleted_file = self._file_repo.delete(file)
                if isinstance(deleted_file, File):
                    deleted_files.append(deleted_file)

        return deleted_files
