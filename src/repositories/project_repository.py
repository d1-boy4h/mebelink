import logging
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..constants import ProjectStatus
from ..models import Project, ProjectDB


class ProjectRepository:
    '''Репозиторий работы с мебельными проектами.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)

    def _to_orm(self, project: Project) -> ProjectDB:
        '''Преобразование модели из Pydantic в ORM.'''

        return ProjectDB(
            uuid=str(project.uuid),
            title=project.title,
            status=project.status.value,
            is_improvements=project.is_improvements,
            created_date=project.created_date,
            start_date=project.start_date,
            end_date=project.end_date,
            address=project.address,
            phone=project.phone
        )

    def _to_pydantic(self, project_db: ProjectDB) -> Project:
        '''Преобразование модели из ORM в Pydantic.'''

        return Project(
            uuid=UUID(project_db.uuid),
            title=project_db.title,
            status=ProjectStatus(project_db.status),
            is_improvements=project_db.is_improvements,
            created_date=project_db.created_date,
            start_date=project_db.start_date,
            end_date=project_db.end_date,
            address=project_db.address,
            phone=project_db.phone
        )

    def save(self, project: Project) -> Project:
        '''Сохранение проекта в базе данных.'''

        project_db = self._to_orm(project)

        with Session(self._engine) as session:
            session.add(project_db)

            try:
                session.commit()
                self._logger.info(
                    f'Проект \'{project.uuid!s}\' сохранён в базу данных'
                )

                return self._to_pydantic(project_db)

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка сохранения проекта \'{project.title}\': {error}'
                )

                raise RuntimeError(f'Ошибка сохранения проекта: {error}')

    def get_by_uuid(self, uuid: UUID) -> Project | None:
        '''Получение проекта по uuid.'''

        with Session(self._engine) as session:
            project_db = session.get(ProjectDB, str(uuid))

            if project_db:
                self._logger.info(
                    f'Проект \'{uuid!s}\' получен из базы данных'
                )
                return self._to_pydantic(project_db)

            return None

    def get_all(self) -> list[Project]:
        '''Получение всех проектов.'''

        with Session(self._engine) as session:
            projects_db = session.execute(select(ProjectDB)).scalars().all()

            if len(projects_db):
                self._logger.info(
                    f'Проектов получено из базы данных: {len(projects_db)}'
                )

            return [self._to_pydantic(project) for project in projects_db]

    def update(self, project: Project) -> Project:
        '''Обновление данных проекта.'''

        with Session(self._engine) as session:
            project_db = session.get(ProjectDB, str(project.uuid))

            if not project_db:
                raise ValueError(f'Проект \'{project.title}\' не найден')

            project_db.title = project.title
            project_db.status = project.status
            project_db.is_improvements = project.is_improvements

            if project.start_date:
                project_db.start_date = project.start_date
            else:
                project_db.start_date = project.created_date

            project_db.end_date = project.end_date
            project_db.address = project.address
            project_db.phone = project.phone

            try:
                session.commit()
                self._logger.info(f'Проект \'{project.uuid!s}\' обновлён')

                return self._to_pydantic(project_db)

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка обновления проекта \'{project.uuid!s}\': {error}'
                )

                raise RuntimeError(f'Ошибка обновления проекта: {error}')

    def delete(self, uuid: UUID) -> Project | None:
        '''Удаление проекта.'''

        with Session(self._engine) as session:
            project_db = session.get(ProjectDB, str(uuid))
            if not project_db: return None

            deleted_project = self._to_pydantic(project_db)

            session.delete(project_db)

            try:
                session.commit()
                self._logger.info(f'Проект \'{uuid!s}\' удалён')

                return deleted_project

            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка удаления проекта \'{id}\': {error}'
                )

                raise RuntimeError(f'Ошибка удаления проекта: {error}')
