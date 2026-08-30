import flet as ft

from ...models import Task


class TaskElement:
    '''Элемент задачи внутри раздела.'''

    def __init__(self, task: Task):
        self._task = task

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        return ft.Text(self._task.title)
