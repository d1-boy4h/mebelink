import io
import json
import logging
from collections.abc import Awaitable, Callable
from datetime import UTC, date, datetime
from uuid import UUID, uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from ..constants import ImportConflictAction, MetaInfo, ProjectStatus
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

    def create_project(self, data: str | Project) -> Project:
        '''Создание проекта.'''

        if isinstance(data, str):
            return self._project_repo.save(Project(title=data))

        else:
            return self._project_repo.save(data)

    def get_by_uuid(self, uuid: UUID) -> Project:
        '''Получение проекта по uuid.'''

        project = self._project_repo.get_by_uuid(uuid)
        if project is None:
            error = ValueError(f'Проект c uuid \'{uuid!s}\' не найден')

            self._logger.error(error)
            raise error

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

    def export_to_mblp(self, project_uuid: UUID) -> bytes:
        '''Экспорт проекта в .mblp файл.'''

        buffer = io.BytesIO()

        project = self.get_by_uuid(project_uuid)

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

        manifest_json = manifest.model_dump_json(indent=2)
        data_json = data.model_dump_json(indent=2)

        try:
            with ZipFile(buffer, 'w', ZIP_DEFLATED) as zf:
                zf.writestr('manifest.json', manifest_json)
                zf.writestr('data.json', data_json)

                for file in files:
                    zf.write(file.path, f'media/{file.filename}')

        except Exception as e:  # noqa: BLE001
            error = RuntimeError(
                f'Ошибка экспорта файла: {e}'
            )
            self._logger.error(error)
            raise error

        return buffer.getvalue()

    async def import_from_mblp(
            self,
            path: str,
            on_conflict: Callable[[], Awaitable[ImportConflictAction]]
        ) -> Project | None:
        '''Импорт проекта из .mblp файла.'''

        action: ImportConflictAction | None = None

        with ZipFile(path, 'r') as zf:
            manifest_json = zf.read('manifest.json').decode('utf-8')
            manifest = json.loads(manifest_json)

            if manifest['format_version'] > int(MetaInfo.MBLP_SCHEMA_VERSION):
                error = TypeError(
                    'Для импрота этого проекта необходимо обновить приложение'
                )

                self._logger.error(error)
                raise error

            same_project = self._project_repo.get_by_uuid(
                manifest['project_uuid']
            )

            if same_project is not None:
                action = await on_conflict()

                match action:
                    case ImportConflictAction.CANCEL:
                        return None
                    case ImportConflictAction.OVERWRITE:
                        self.delete_project(manifest['project_uuid'])

            data_json = zf.read('data.json').decode('utf-8')
            data = json.loads(data_json)

        project_data = data['project']

        uuid = UUID(project_data['uuid'])
        title = project_data['title']
        end_date = project_data['end_date']

        if action is not None and action == ImportConflictAction.DUPLICATE:
            uuid = uuid4()
            title = title + ' (копия)'

        project_model = Project(
            uuid=uuid,
            title=title,
            status=ProjectStatus(project_data['status']),
            is_improvements=project_data['is_improvements'],
            created_date=datetime.fromisoformat(
                project_data['created_date']
            ),
            start_date=date.fromisoformat(
                project_data['start_date']
            ),
            end_date=date.fromisoformat(end_date) if end_date else None,
            address=project_data['address'],
            phone=project_data['phone']
        )

        new_project = self.create_project(project_model)

        tag_id_map: dict[int, int] = {}

        for tag_data in data['task_tags']:
            old_id = tag_data['id']
            new_tag = self._tag_service.create(
                title=tag_data['title'],
                project_uuid=new_project.uuid,
            )

            if new_tag.is_open != tag_data['is_open']:
                new_tag.is_open = tag_data['is_open']
                new_tag = self._tag_service.update(new_tag)

            if new_tag.id is not None:
                tag_id_map[old_id] = new_tag.id

        for task_data in data['tasks']:
            old_tag_id = task_data['task_tag_id']

            new_tag_id = tag_id_map.get(old_tag_id)
            if new_tag_id is None:
                self._logger.warning(
                    f'Пропущена задача \'{task_data["title"]}\': '
                    f'раздел с id {old_tag_id} не найден'
                )
                continue

            new_task = self._task_service.create(
                title=task_data['title'],
                tag_id=new_tag_id,
            )

            if new_task.is_completed != task_data['is_completed']:
                new_task.is_completed = task_data['is_completed']
                self._task_service.update(new_task)

        for note_data in data['notes']:
            new_note = self._note_service.create(
                title=note_data['title'],
                project_uuid=new_project.uuid,
            )

            needs_update = False
            if new_note.desc != note_data['desc']:
                new_note.desc = note_data['desc']
                needs_update = True
            if new_note.is_open != note_data['is_open']:
                new_note.is_open = note_data['is_open']
                needs_update = True

            if needs_update:
                self._note_service.update(new_note)

        with ZipFile(path, 'r') as zf:
            for file_data in data['files']:
                filename = file_data['filename']
                media_name = f'media/{filename}'

                if media_name not in zf.namelist():
                    self._logger.warning(
                        f'Файл \'{filename}\' отсутствует в архиве, пропущен'
                    )
                    continue

                content = zf.read(media_name)

                try:
                    self._file_service.save_file(
                        project_uuid=new_project.uuid,
                        name=filename,
                        content=content,
                    )
                except ValueError as e:
                    self._logger.warning(f'Не удалось сохранить файл: {e}')

        log_text = f'Проект \'{new_project.title}\' был '
        match action:
            case None:
                log_text += 'экспортирован'
            case ImportConflictAction.DUPLICATE:
                log_text += 'дублирован'
            case ImportConflictAction.OVERWRITE:
                log_text += 'перезаписан'

        self._logger.info(log_text)

        return new_project
