from collections.abc import Callable

import flet as ft

from ...constants import ColorPalette
from ...models import Task
from ...services import TaskService


class TaskElement:
    '''Элемент задачи внутри раздела.'''

    def __init__(
        self,
        task: Task,
        page: ft.Page,
        task_service: TaskService,
        refresh_list_callback: Callable
    ):
        self._task = task
        self._page = page
        self._task_service = task_service
        self._refresh_list_callback = refresh_list_callback

        self.__is_editing: bool = False

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        self._title = ft.Text(
            self._task.title,
            expand=True,
            size=16,
            color='#000',
            weight=ft.FontWeight.NORMAL,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH
            ),
        )

        self._title_wrapper = ft.Container(self._title, expand=True)

        self._checkbox = ft.Checkbox(
            value=self._task.is_completed,
            active_color=ColorPalette.MAIN,
            scale=1.2,
            border_side=ft.BorderSide(width=1, color='#000'),
            on_change=self._on_change_checkbox,
            visible=not self._is_editing
        )

        title_and_checkbox = ft.Row(
            controls=[self._title_wrapper, self._checkbox],
            spacing=0
        )

        cancel_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ColorPalette.MAIN,
            icon_size=24,
            on_click=lambda _: setattr(self, '_is_editing', False)
        )

        self._rename_btn = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ColorPalette.GRAY,
            icon_size=24,
            disabled=True,
            on_click=lambda: self._rename(self._title_input.value)
        )

        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ColorPalette.RED,
            icon_size=24,
            on_click=self._delete
        )

        self._buttons = ft.Row(
            controls=[delete_btn, self._rename_btn, cancel_btn],
            spacing=0,
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            visible=False
        )

        self._on_change_checkbox(dont_update=True)

        return ft.ElevatedButton(
            content=ft.Column([title_and_checkbox, self._buttons], spacing=0),
            expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.Padding(20, 20, 10, 20)),
            on_click=self._on_click,
            on_long_press=lambda _: setattr(
                self, '_is_editing', not self._is_editing
            )
        )

    def _on_click(self, _):
        '''Обработка нажатия на всю задачу.'''

        self._checkbox.value = not self._checkbox.value
        self._on_change_checkbox()

    def _on_change_checkbox(self, _ = None, dont_update: bool = False):
        '''Обработка нажания чекбокса.'''

        state = self._checkbox.value

        if isinstance(state, bool):
            self._task.is_completed = state

            if not dont_update:
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

    def _refresh(self):
        '''Сброс компонента по умолчанию.'''

        self._title.value = self._task.title
        self._title_wrapper.content = self._title
        self._checkbox.visible = True
        self._buttons.visible = False

    @property
    def _is_editing(self):
        return self.__is_editing

    @_is_editing.setter
    def _is_editing(self, value: bool):
        '''Обработка режима редактирования.'''

        if value and not self._is_editing:
            self._title_input = ft.TextField(
                hint_text=self._task.title,
                text_size=16,
                value=self._task.title,
                autofocus=True,
                multiline=True,
                border=ft.InputBorder.NONE,
                content_padding=0,
                expand=True,
                on_change=self._on_input_change
            )

            self._title_wrapper.content = self._title_input
            self._checkbox.visible = False
            self._buttons.visible = True

        else:
            self._refresh()

        self.__is_editing = value

    def _rename(self, title: str):
        '''Переименование задачи.'''

        if title.strip() and title != self._task.title:
            self._task.title = title
            self._task_service.update(self._task)

        self._is_editing = False

        self._rename_btn.icon_color = ColorPalette.GRAY
        self._rename_btn.disabled = True

    def _delete(self):
        '''Удаление задачи.'''

        self._task_service.delete(self._task)
        self._refresh_list_callback()

    def _on_input_change(self, e: ft.Event[ft.TextField]):
        '''Обработка изменения input'a для видимости кнопки переименования.'''

        if not isinstance(e.data, str):
            return

        if e.data != self._task.title and e.data.strip() != '':
            self._rename_btn.icon_color = ColorPalette.MAIN
            self._rename_btn.disabled = False

        else:
            self._rename_btn.icon_color = ColorPalette.GRAY
            self._rename_btn.disabled = True
