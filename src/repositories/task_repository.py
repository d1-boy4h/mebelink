import logging

from sqlalchemy import Engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import Task, TaskDB, TaskTag


class TaskRepository:
    '''Репозиторий работы с задачами проектов.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)

    def _to_orm(self, task: Task) -> TaskDB:
        '''Преобразование модели из Pydantic в ORM.'''

        return TaskDB(
            task_tag_id=task.task_tag_id,
            title=task.title,
            is_completed=task.is_completed
        )

    def _to_pydantic(self, task_db: TaskDB) -> Task:
        '''Преобразование модели из ORM в Pydantic.'''

        return Task(
            id=task_db.id,
            task_tag_id=task_db.task_tag_id,
            title=task_db.title,
            is_completed=task_db.is_completed
        )

    def save(self, task: Task) -> Task:
        '''Сохранение задачи в базе данных.'''

        task_db = self._to_orm(task)

        with Session(self._engine) as session:
            session.add(task_db)

            try:
                session.commit()
                session.refresh(task_db)

                self._logger.info(
                    f'Задача \'{task.title}\' сохранена в базу данных'
                )

                return self._to_pydantic(task_db)

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка сохранения задачи \'{task.title}\': {e}'
                )

                self._logger.error(error)
                raise error

    def get_by_id(self, task_id: int) -> Task | None:
        '''Получение задачи по идентификатору.'''

        with Session(self._engine) as session:
            task_db = session.get(TaskDB, task_id)

            if task_db:
                self._logger.info(
                    f'Задача \'{task_db.title}\' получена из базы данных'
                )
                return self._to_pydantic(task_db)

            return None 

    def get_by_task_tag(self, tag: TaskTag) -> list[Task]:
        '''Получение всех задач раздела.'''

        with Session(self._engine) as session:
            tasks_db = session.execute(
                select(TaskDB).where(TaskDB.task_tag_id == tag.id)
            ).scalars().all()

            if len(tasks_db):
                self._logger.info(
                    f'Задач раздела \'{tag.title}\' получено из базы данных: {len(tasks_db)}'
                )

            return [self._to_pydantic(task) for task in tasks_db]

    def update(self, task: Task) -> Task:
        '''Обновление данных задачи.'''

        with Session(self._engine) as session:
            task_db = session.get(TaskDB, task.id)

            if not task_db:
                e = ValueError(f'Задача \'{task.title}\' не найдена')

                self._logger.error(e)
                raise e

            task_db.task_tag_id=task.task_tag_id
            task_db.title=task.title
            task_db.is_completed=task.is_completed

            try:
                session.commit()
                self._logger.info(f'Задача \'{task.title}\' обновлена')

                return self._to_pydantic(task_db)

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка обновления задачи \'{task.title}\': {e}'
                )

                self._logger.error(error)
                raise error

    def delete(self, task_id: int) -> Task | None:
        '''Удаление файла.'''

        with Session(self._engine) as session:
            task_db = session.get(TaskDB, task_id)
            if not task_db: return None

            deleted_task = self._to_pydantic(task_db)

            session.delete(task_db)

            try:
                session.commit()
                self._logger.info(f'Задача \'{deleted_task.title}\' удалена')

                return deleted_task

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка удаления задачи \'{task_id}\': {e}'
                )

                self._logger.error(error)
                raise error
