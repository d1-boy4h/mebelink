import logging

from sqlalchemy import Engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import TaskTag, TaskTagDB


class TaskTagRepository:
    '''Репозиторий работы с разделами задач.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger(__name__)

    def _to_orm(self, tag: TaskTag) -> TaskTagDB:
        '''Преобразование модели из Pydantic в ORM.'''
        return TaskTagDB(title=tag.title, is_open=tag.is_open)

    def _to_pydantic(self, tag_db: TaskTagDB) -> TaskTag:
        '''Преобразование модели из ORM в Pydantic.'''

        return TaskTag(
            title=tag_db.title,
            is_open=tag_db.is_open
        )

    def save(self, tag: TaskTag) -> TaskTag:
        '''Сохранение раздела в базе данных.'''

        tag_db = self._to_orm(tag)

        with Session(self._engine) as session:
            session.add(tag_db)

            try:
                session.commit()
                session.refresh(tag_db)

                self._logger.info(
                    f'Раздел \'{tag.title}\' сохранён в базу данных'
                )

                return self._to_pydantic(tag_db)

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка сохранения раздела \'{tag.title}\': {error}'
                )

                raise RuntimeError(f'Ошибка сохранения раздела: {error}')

    def is_exist(self, title: str) -> bool:
        '''Существует ли раздел с таким названием.'''

        with Session(self._engine) as session:
            tag_db = session.execute(
                select(TaskTagDB).where(TaskTagDB.title == title)
            ).scalar_one_or_none()

            return tag_db is not None

    def get_all(self) -> list[TaskTag]:
        '''Получение всех разделов.'''

        with Session(self._engine) as session:
            tags_db = session.execute(select(TaskTagDB)).scalars().all()

            if len(tags_db):
                self._logger.info(
                    f'Разделов получено из базы данных: {len(tags_db)}'
                )

            return [self._to_pydantic(tag_db) for tag_db in tags_db]

    def update(self, tag: TaskTag) -> TaskTag:
        '''Обновление данных раздела.'''

        with Session(self._engine) as session:
            tag_db = session.get(TaskTagDB, tag.title)

            if not tag_db:
                raise ValueError(f'Раздел \'{tag.title}\' не найден')

            tag_db.title = tag.title
            tag_db.is_open = tag.is_open

            try:
                session.commit()
                self._logger.info(f'Раздел \'{tag.title}\' обновлён')

                return self._to_pydantic(tag_db)

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка обновления раздела \'{tag.title}\': {error}'
                )

                raise RuntimeError(f'Ошибка обновления раздела: {error}')

    def delete(self, tag_id: int) -> TaskTag | None:
        '''Удаление раздела.'''

        with Session(self._engine) as session:
            tag_db = session.get(TaskTagDB, tag_id)
            if not tag_db: return None

            deleted_file = self._to_pydantic(tag_db)

            session.delete(tag_db)

            try:
                session.commit()
                self._logger.info(f'Раздел \'{tag_db.title}\' удалён')

                return deleted_file

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка удаления раздела \'{tag_db.title}\': {error}'
                )

                raise RuntimeError(f'Ошибка удаления раздела: {error}')
