import flet as ft

from ...store import store


class TasksTab:
    '''Вкладка с задачами проекта.'''

    def __init__(self):
        pass

    def build(self) -> ft.Control:
        '''Сборка интерфейса вкладки.'''

        self._project = store.current_project
        if self._project is None:
            raise RuntimeError('Такого проекта не существует')

        return ft.ListView([
            ft.Text('Вкладка задач')
        ], spacing=20)
