import logging
from datetime import UTC, datetime
from uuid import UUID
from zipfile import ZIP_DEFLATED, ZipFile

from ..constants import MetaInfo, ProjectStatus
from ..models import Data, Manifest, Project
from ..repositories import ProjectRepository
from .file_service import FileService
from .note_service import NoteService
from .task_service import TaskService
from .task_tag_service import TaskTagService


class ProjectService:
    '''Сервис работы с мебельными проектами.'''

    def __init__(
        self,
        project_repo: ProjectRepository,
        file_service: FileService,
        tag_service: TaskTagService,
        task_service: TaskService,
        note_service: NoteService
    ):
        self._project_repo = project_repo
        self._file_service = file_service
        self._tag_service = tag_service
        self._note_service = note_service
        self._task_service = task_service

        self._logger = logging.getLogger(self.__class__.__name__)

    def create_project(self, title: str) -> Project:
        '''Создание проекта.'''
        return self._project_repo.save(Project(title=title))

    def get_by_uuid(self, uuid: UUID) -> Project:
        '''Получение проекта по uuid.'''

        project = self._project_repo.get_by_uuid(uuid)
        if project is None:
            raise ValueError(f'Проект c uuid \'{uuid!s}\' не найден')

        return project

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

        self._file_service.delete_project_files(project_uuid)
        self._tag_service.delete_project_tags(project_uuid)
        self._note_service.delete_project_notes(project_uuid)

        return self._project_repo.delete(project_uuid)

    def export_to_mblp(self, project_uuid: UUID, path: str) -> str:
        '''Экспорт проекта в .mblp файл.'''

        project = self.get_by_uuid(project_uuid)

        if project is None:
            raise ValueError(f'Проект c uuid \'{project_uuid!s}\' не найден')

        manifest = Manifest(
            format_version=int(MetaInfo.MBLP_SCHEMA_VERSION),
            project_uuid=project.uuid,
            project_title=project.title,
            exported_at=datetime.now(tz=UTC)
        )

        tags = self._tag_service.get_all(project.uuid)

        tasks = []
        for tag in tags:
            task_group = self._task_service.get_all(tag)
            tasks.extend(task_group)

        files = self._file_service.get_all(project.uuid)

        data = Data(
            project=project,
            files=files,
            task_tags=tags,
            tasks=tasks,
            notes=self._note_service.get_all(project.uuid)
        )

        valid_path = path
        if not path.endswith('.mblp'):
            valid_path = path + '.mblp'

        manifest_json = manifest.model_dump_json(indent=2)
        data_json = data.model_dump_json(indent=2)

        try:
            with ZipFile(valid_path, 'w', ZIP_DEFLATED) as zf:
                zf.writestr('manifest.json', manifest_json)
                zf.writestr('data.json', data_json)

                for file in files:
                    zf.write(file.path, f'media/{file.filename}')

        except Exception as e:  # noqa: BLE001
            self._logger.error(e)
            raise RuntimeError('Ошибка экспорта файла (подробности в логах)')

        return path
