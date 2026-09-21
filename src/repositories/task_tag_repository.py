import logging
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import TaskTag, TaskTagDB


class TaskTagRepository:
    '''Репозиторий работы с разделами задач.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)

    def _to_orm(self, tag: TaskTag) -> TaskTagDB:
        '''Преобразование модели из Pydantic в ORM.'''

        return TaskTagDB(
            title=tag.title,
            project_uuid=str(tag.project_uuid),
            is_open=tag.is_open
        )

    def _to_pydantic(self, tag_db: TaskTagDB) -> TaskTag:
        '''Преобразование модели из ORM в Pydantic.'''

        return TaskTag(
            id=tag_db.id,
            title=tag_db.title,
            project_uuid=UUID(tag_db.project_uuid),
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

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка сохранения раздела \'{tag.title}\': {e}'
                )

                self._logger.error(error)
                raise error

    def get_by_id(self, tag_id: int) -> TaskTag | None:
        '''Получение раздела по идентификатору.'''

        with Session(self._engine) as session:
            tag_db = session.get(TaskTagDB, tag_id)

            if tag_db:
                self._logger.info(
                    f'Раздел \'{tag_db.title}\' получен из базы данных'
                )
                return self._to_pydantic(tag_db)

            return None

    def get_by_project(self, project_uuid: UUID) -> list[TaskTag]:
        '''Получение всех разделов проекта.'''

        with Session(self._engine) as session:
            tags_db = session.execute(
                select(TaskTagDB).where(TaskTagDB.project_uuid == str(project_uuid))
            ).scalars().all()

            if len(tags_db):
                self._logger.info(
                    f'Разделов получено из базы данных: {len(tags_db)}'
                )

            return [self._to_pydantic(tag) for tag in tags_db]

    def update(self, tag: TaskTag) -> TaskTag:
        '''Обновление данных раздела.'''

        with Session(self._engine) as session:
            tag_db = session.get(TaskTagDB, tag.id)

            if not tag_db:
                e = ValueError(f'Раздел \'{tag.title}\' не найден')

                self._logger.error(e)
                raise e

            tag_db.title = tag.title
            tag_db.project_uuid = str(tag.project_uuid)
            tag_db.is_open = tag.is_open

            try:
                session.commit()
                self._logger.info(f'Раздел \'{tag.title}\' обновлён')

                return self._to_pydantic(tag_db)

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка обновления раздела \'{tag.title}\': {e}'
                )

                self._logger.error(error)
                raise error

    def delete(self, tag_id: int) -> TaskTag | None:
        '''Удаление раздела.'''

        with Session(self._engine) as session:
            tag_db = session.get(TaskTagDB, tag_id)
            if not tag_db: return None

            deleted_tag = self._to_pydantic(tag_db)

            session.delete(tag_db)

            try:
                session.commit()
                self._logger.info(f'Раздел \'{deleted_tag.title}\' удалён')

                return deleted_tag

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка удаления раздела \'{tag_db.title}\': {e}'
                )

                self._logger.error(error)
                raise error
