import logging
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import File, FileDB


class FileRepository:
    '''Репозиторий работы с файлами мебельных проектов.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)

    def _to_orm(self, file: File) -> FileDB:
        '''Преобразование модели из Pydantic в ORM.'''

        return FileDB(
            project_uuid=str(file.project_uuid),
            filename=file.filename,
            path=file.path,
            uploaded_date=file.uploaded_date
        )

    def _to_pydantic(self, file_db: FileDB) -> File:
        '''Преобразование модели из ORM в Pydantic.'''

        return File(
            id=file_db.id,
            project_uuid=UUID(file_db.project_uuid),
            filename=file_db.filename,
            path=file_db.path,
            uploaded_date=file_db.uploaded_date
        )

    def save(self, file: File) -> File:
        '''Сохранение файла в базе данных.'''

        file_db = self._to_orm(file)

        with Session(self._engine) as session:
            session.add(file_db)

            try:
                session.commit()
                session.refresh(file_db)

                self._logger.info(
                    f'Файл \'{file.filename}\' сохранён в базу данных'
                )

                return self._to_pydantic(file_db)

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка сохранения файла \'{file.filename}\': {error}'
                )

                raise RuntimeError(f'Ошибка сохранения файла: {error}')

    def get_by_id(self, file_id: int) -> File | None:
        '''Получение файла по id.'''

        with Session(self._engine) as session:
            file_db = session.get(FileDB, file_id)

            if file_db:
                self._logger.info(
                    f'Файл \'{file_db.filename}\' получен из базы данных'
                )
                return self._to_pydantic(file_db)

            return None

    def get_by_project(self, project_uuid: UUID) -> list[File]:
        '''Получение всех файлов проекта.'''

        with Session(self._engine) as session:
            files_db = session.execute(
                select(FileDB).where(FileDB.project_uuid == str(project_uuid))
            ).scalars().all()

            if len(files_db):
                self._logger.info(
                    f'Файлов получено из базы данных: {len(files_db)}'
                )

            return [self._to_pydantic(file) for file in files_db]

    def update(self, file: File) -> File:
        '''Обновление данных файла.'''

        with Session(self._engine) as session:
            file_db = session.get(FileDB, file.id)

            if not file_db:
                raise ValueError(f'Файл \'{file.filename}\' не найден')

            file_db.project_uuid = str(file.project_uuid)
            file_db.filename = file.filename
            file_db.path = file.path
            file_db.uploaded_date = file.uploaded_date

            try:
                session.commit()
                self._logger.info(f'Файл \'{file.filename}\' обновлён')

                return self._to_pydantic(file_db)

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка обновления файла \'{file.filename}\': {error}'
                )

                raise RuntimeError(f'Ошибка обновления файла: {error}')

    def delete(self, file: File) -> File | None:
        '''Удаление файла.'''

        with Session(self._engine) as session:
            file_db = session.get(FileDB, file.id)
            if not file_db: return None

            deleted_file = self._to_pydantic(file_db)

            session.delete(file_db)

            try:
                session.commit()
                self._logger.info(f'Файл \'{file.filename}\' удалён')

                return deleted_file

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка удаления Файла \'{file.filename}\': {error}'
                )

                raise RuntimeError(f'Ошибка удаления файла: {error}')
