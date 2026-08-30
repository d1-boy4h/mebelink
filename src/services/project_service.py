from uuid import UUID

from ..constants import ProjectStatus
from ..models import Project
from ..repositories import ProjectRepository
from .file_service import FileService
from .task_tag_service import TaskTagService


class ProjectService:
    '''Сервис работы с мебельными проектами.'''

    def __init__(
        self,
        project_repo: ProjectRepository,
        file_service: FileService,
        tag_service: TaskTagService
    ):
        self._project_repo = project_repo
        self._file_service = file_service
        self._tag_service = tag_service

    def create_project(self, title: str) -> Project:
        '''Создание проекта.'''
        return self._project_repo.save(Project(title=title))

    def get_by_uuid(self, uuid: UUID) -> Project | None:
        '''Получение проекта по uuid.'''
        return self._project_repo.get_by_uuid(uuid)

    def get_all(self) -> list[Project]:
        '''Получение всех проектов.'''

        projects = self._project_repo.get_all()

        # TODO: Пока временная сортировка, потом переделать в полноценную
        projects.sort(key=lambda p: p.status == ProjectStatus.COMPLETED)

        return projects

    def update_project(self, project: Project) -> Project:
        '''Обновление данных проекта.'''
        return self._project_repo.update(project)

    def delete_project(self, project_uuid: UUID) -> Project | None:
        '''Удаление проекта.'''

        project = self._project_repo.get_by_uuid(project_uuid)
        if not project:
            raise ValueError(f'Проект c uuid \'{project_uuid!s}\' не найден')

        if project is not None:
            self._file_service.delete_project_files(project_uuid)
            self._tag_service.delete_project_tags(project_uuid)

            return self._project_repo.delete(project_uuid)
