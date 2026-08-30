from uuid import UUID

from ..models import TaskTag
from ..repositories import TaskTagRepository
from .task_service import TaskService


class TaskTagService:
    '''Сервис работы с разделами задач.'''

    def __init__(self, tag_repo: TaskTagRepository, task_service: TaskService):
        self._tag_repo = tag_repo
        self._task_service = task_service

    def create(self, title: str, project_uuid: UUID) -> TaskTag:
        '''Создание раздела.'''

        return self._tag_repo.save(TaskTag(
            title=title, project_uuid=project_uuid
        ))

    def get_all(self, project_uuid: UUID) -> list[TaskTag]:
        '''Получение всех разделов проекта.'''
        return self._tag_repo.get_by_project(project_uuid)

    def update(self, tag: TaskTag) -> TaskTag:
        '''Обновление данных раздела (открытие, закрытие и переименование).'''
        return self._tag_repo.update(tag)

    def delete_tag(self, tag: TaskTag) -> TaskTag | None:
        '''Удаление раздела.'''

        if tag.id is None:
            return None

        self._task_service.delete_tag_tasks(tag)
        return self._tag_repo.delete(tag.id)

    def delete_project_tags(self, project_uuid: UUID) -> list[TaskTag]:
        '''Удаление всех разделов проекта.'''

        tags = self._tag_repo.get_by_project(project_uuid)
        deleted_files = []
        for tag in tags:
            if tag.id is not None:
                deleted_tag = self._tag_repo.delete(tag.id)
                if isinstance(deleted_tag, TaskTag):
                    deleted_files.append(deleted_tag)

        return deleted_files
