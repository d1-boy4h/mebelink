from ..models import Task
from ..repositories import TaskRepository


class TaskService:
    '''Сервис работы с разделами задач.'''

    def __init__(self, task_repo: TaskRepository):
        self._task_repo = task_repo


    def create(self, title: str, tag_id: int) -> Task:
        '''Создание задачи.'''
        return self._task_repo.save(Task(title=title, task_tag_id=tag_id))

    def get_all(self, tag_id: int) -> list[Task]:
        '''Получение всех задач раздела.'''
        return self._task_repo.get_by_task_tag(tag_id)

    def update(self, tag: Task) -> Task:
        '''Обновление данных задачи.'''
        return self._task_repo.update(tag)

    def delete(self, task_id: int) -> Task | None:
        '''Удаление задачи.'''

        task = self._task_repo.get_by_id(task_id)
        if not task:
            raise ValueError(f'Задача c id \'{task_id}\' не найдена')

        return self._task_repo.delete(task_id)
