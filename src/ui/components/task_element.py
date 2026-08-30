import flet as ft

from ...constants import ColorPalette
from ...models import Task
from ...services import TaskService


class TaskElement:
    '''Элемент задачи внутри раздела.'''

    def __init__(self, task: Task, task_service: TaskService):
        self._task = task
        self._task_service = task_service

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        self._title = ft.Text(
            self._task.title,
            expand=True,
            size=16,
            color='#000',
            weight=ft.FontWeight.NORMAL,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                # decoration_thickness=3,
            ),
        )

        self._checkbox = ft.Checkbox(
            value=self._task.is_completed,
            active_color=ColorPalette.MAIN,
            scale=1.2,
            border_side=ft.BorderSide(width=1, color='#000'),
            on_change=self._on_change_checkbox
        )

        self._on_change_checkbox()

        return ft.ElevatedButton(
            content=ft.Row([self._title, self._checkbox], spacing=0),
            expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.Padding(20, 20, 10, 20)),
            on_click=self._on_click
            # on_long_press=
        )

    def _on_click(self, _):
        '''Обработка нажатия на всю задачу.'''

        self._checkbox.value = not self._checkbox.value
        self._on_change_checkbox()

    def _on_change_checkbox(self, _ = None):
        '''Обработка нажания чекбокса.'''

        state = self._checkbox.value

        if isinstance(state, bool):
            self._task.is_completed = state
            self._task_service.update(self._task)

            if state:
                self._checkbox.border_side = ft.BorderSide()
                self._title.color = ColorPalette.GRAY
                self._title.style = ft.TextStyle(
                    decoration=ft.TextDecoration.LINE_THROUGH
                )
            else:
                self._title.style = None
                self._title.color = '#000'
                self._checkbox.border_side = ft.BorderSide(
                    width=1, color='#000'
                )