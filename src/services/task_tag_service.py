from ..models import TaskTag
from ..repositories import TaskTagRepository


class TaskTagService:
    '''Сервис работы с разделами задач.'''

    def __init__(self, task_tag_repo: TaskTagRepository):
        self._task_tag_repo = task_tag_repo

    def create(self, title: str) -> TaskTag:
        '''Создание раздела.'''

        if not self._task_tag_repo.is_exist(title):
            return self._task_tag_repo.save(TaskTag(title=title))

        else:
            raise ValueError(f'Раздел \'{title}\' уже существует')

    def get_all(self) -> list[TaskTag]:
        '''Получение всех разделов.'''
        return self._task_tag_repo.get_all()

    def update(self, tag: TaskTag) -> TaskTag:
        '''Обновление данных раздела (открытие, закрытие и переименование).'''
        return self._task_tag_repo.update(tag)

    def delete(self, tag_id: int) -> TaskTag | None:
        '''Удаление раздела.'''
        return self._task_tag_repo.delete(tag_id)
