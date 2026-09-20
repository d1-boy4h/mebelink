from collections.abc import Callable

import flet as ft

from .....constants import ColorPalette
from .....services import TaskService


class TaskCreationButton:
    '''Элемент задачи внутри раздела.'''

    def __init__(
        self,
        tag_id: int,
        task_service: TaskService,
        refresh_list_callback: Callable
    ):
        self._tag_id = tag_id
        self._task_service = task_service
        self._refresh_list_callback = refresh_list_callback

        self.__is_creating = False

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        self._add_btn = ft.Button(
            content=ft.Text('+', size=20, color=ColorPalette.MAIN),
            expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda _: setattr(self, 'is_creating', True)
        )

        self._container = ft.Row([self._add_btn])

        return self._container

    @property
    def is_creating(self):
        return self.__is_creating

    @is_creating.setter
    def is_creating(self, value: bool):
        '''Обработка режима создания.'''

        if value and not self.is_creating:
            self._title_input = ft.TextField(
                hint_text='Новая задача',
                text_size=16,
                autofocus=True,
                border=ft.InputBorder.NONE,
                content_padding=0,
                expand=True
            )

            cancel_btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ColorPalette.MAIN,
                on_click=lambda _: setattr(self, 'is_creating', False)
            )

            confirm_btn = ft.IconButton(
                icon=ft.Icons.CHECK,
                icon_color=ColorPalette.GREEN,
                on_click=lambda _: self._create_task(self._title_input.value)
            )

            buttons = ft.Row([cancel_btn, confirm_btn], spacing=5)
            self._container.controls = [
                self._title_input, buttons
            ]

        else:
            self._container.controls = [self._add_btn]

        self.__is_creating = value

    def _create_task(self, title: str):
        '''Создание задачи.'''

        self.is_creating = False
        self._task_service.create(title, self._tag_id)
        self._refresh_list_callback()
