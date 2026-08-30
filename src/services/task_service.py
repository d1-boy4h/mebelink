from ..models import Task, TaskTag
from ..repositories import TaskRepository


class TaskService:
    '''Сервис работы с разделами задач.'''

    def __init__(self, task_repo: TaskRepository):
        self._task_repo = task_repo


    def create(self, title: str, tag_id: int) -> Task:
        '''Создание задачи.'''
        return self._task_repo.save(Task(title=title, task_tag_id=tag_id))

    def get_all(self, tag: TaskTag) -> list[Task]:
        '''Получение всех задач раздела.'''
        return self._task_repo.get_by_task_tag(tag)

    def update(self, task: Task) -> Task:
        '''Обновление данных задачи.'''
        return self._task_repo.update(task)

    def delete(self, task: Task) -> Task | None:
        '''Удаление задачи.'''

        if task.id is None:
            return None

        return self._task_repo.delete(task.id)

    def delete_tag_tasks(self, tag: TaskTag) -> list[Task]:
        '''Удаление всех задач раздела.'''

        tasks = self._task_repo.get_by_task_tag(tag)
        deleted_tasks = []
        for task in tasks:
            if task.id is not None:
                deleted_task = self._task_repo.delete(task.id)

                if isinstance(deleted_task, Task):
                    deleted_tasks.append(deleted_task)

        return deleted_tasks
