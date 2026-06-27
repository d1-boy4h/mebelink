from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import logging

from ..models import Project, ProjectDB
from ..constants import ProjectStatus

class ProjectRepository:
    '''Репозиторий работы с мебельными проектами.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger('ProjectRepository')

    def _to_orm(self, project: Project) -> ProjectDB:
        '''Преобразование Pydantic-модели в ORM.'''
        return ProjectDB(
            uuid=str(project.uuid),
            title=project.title,
            status=project.status.value,
            is_improvements=project.is_improvements,
            created_date=project.created_date,
            start_date=project.start_date,
            end_date=project.end_date
        )

    def _to_pydantic(self, project_db: ProjectDB) -> Project:
        '''Преобразование ORM-модели в Pydantic.'''
        return Project(
            uuid=UUID(project_db.uuid),
            title=project_db.title,
            status=ProjectStatus(project_db.status),
            is_improvements=project_db.is_improvements,
            created_date=project_db.created_date,
            start_date=project_db.start_date,
            end_date=project_db.end_date
        )

    def save(self, project: Project) -> Project:
        '''Сохранение проекта в базе данных.'''
        project_db = self._to_orm(project)

        with Session(self._engine) as session:
            session.add(project_db)

            try:
                session.commit()
                self._logger.info(
                    f'Проект \'{str(project.uuid)}\' сохранён в базу данных'
                )

                return self._to_pydantic(project_db)
            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка сохранения проекта \'{str(project.uuid)}\': {error}'
                )
                raise RuntimeError(f'Ошибка сохранения проекта: {error}')
    
    def get_by_uuid(self, uuid: UUID) -> Project | None:
        '''Получение проекта по uuid.'''
        with Session(self._engine) as session:
            project_db = session.get(ProjectDB, str(uuid))

            if project_db:
                self._logger.info(
                    f'Проект \'{str(uuid)}\' получен из базы данных'
                )
                return self._to_pydantic(project_db)
            
            return None

    def get_all(self) -> list[Project]:
        '''Получение всех проектов.'''
        with Session(self._engine) as session:
            projects_db = session.execute(select(ProjectDB)).scalars().all()

            self._logger.info(
                f'Проектов получено из базы данных: {len(projects_db)}'
            )
            return [self._to_pydantic(project) for project in projects_db]

    def update(self, project: Project) -> Project:
        '''Обновление данных проекта.'''
        with Session(self._engine) as session:
            project_db = session.get(ProjectDB, str(project.uuid))

            if not project_db:
                raise ValueError(f'Проект \'{str(project.uuid)}\' не найден')

            project_db.title = project.title
            project_db.status = project.status
            project_db.is_improvements = project.is_improvements
            project_db.start_date = project.start_date
            project_db.end_date = project.end_date

            try:
                session.commit()
                self._logger.info(
                    f'Проект \'{str(project.uuid)}\' обновлён'
                )

                return self._to_pydantic(project_db)
            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка обновления проекта \'{str(project.uuid)}\': {error}'
                )
                raise RuntimeError(f'Ошибка обновления проекта: {error}')

    def delete(self, uuid: UUID) -> Project | None:
        '''Удаление проекта.'''
        with Session(self._engine) as session:
            project_db = session.get(ProjectDB, str(uuid))

            if not project_db:
                return None

            deleted_project = self._to_pydantic(project_db)

            session.delete(project_db)

            try:
                session.commit()
                self._logger.info(
                    f'Проект \'{str(uuid)}\' удалён'
                )

                return deleted_project
            except SQLAlchemyError as error:
                session.rollback()
                self._logger.error(
                    f'Ошибка удаления проекта \'{id}\': {error}'
                )
                raise RuntimeError(f'Ошибка удаления проекта: {error}')
