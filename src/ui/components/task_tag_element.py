from collections.abc import Callable

import flet as ft

from ...constants import ColorPalette
from ...models import TaskTag
from ...services import TaskService, TaskTagService
from .task_creation_button import TaskCreationButton
from .task_element import TaskElement


class TaskTagElement:
    '''Элемент выпадающего списка (раздела) с задачами проекта.'''

    def __init__(
            self,
            tag: TaskTag,
            page: ft.Page,
            task_tag_service: TaskTagService,
            task_service: TaskService,
            refresh_list_callback: Callable
        ):
        self._tag = tag

        self._page = page
        self._task_tag_service = task_tag_service
        self._task_service = task_service
        self._refresh_list_callback = refresh_list_callback

        self.__is_deleting: bool = False
        self.__is_editing: bool = False

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        self._title = ft.Text(
            self._tag.title,
            expand=True
        )

        self._edit_btn = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ColorPalette.MAIN,
            on_click=lambda _: setattr(self, '_is_editing', True)
        )

        self._delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ColorPalette.RED,
            on_click=lambda _: setattr(self, '_is_deleting', True)
        )

        self._buttons = ft.Row(
            controls=[self._edit_btn, self._delete_btn],
            spacing=0,
            visible=self._tag.is_open
        )

        self._tile_title_wrapper = ft.Row(
            controls=[self._title, self._buttons],
            spacing=0
        )

        self._task_list = ft.Column([], spacing=10)
        self._refresh_task_list()

        return ft.ExpansionTile(
            title=self._tile_title_wrapper,
            controls=[self._task_list],
            bgcolor='#fff',
            collapsed_bgcolor='#fff',
            shape=ft.RoundedRectangleBorder(radius=10),
            collapsed_shape=ft.RoundedRectangleBorder(radius=10),
            controls_padding=ft.Padding(20, 15, 20, 10),
            on_change=self._switch_tag_handler,
            expanded=self._tag.is_open
        )

    def _refresh(self):
        '''Сброс компонента по умолчанию.'''

        self._title.value = self._tag.title
        self._title.color = None

        self._edit_btn.icon = ft.Icons.EDIT
        self._edit_btn.icon_color = ColorPalette.MAIN

        self._buttons.controls = [self._edit_btn, self._delete_btn]
        self._tile_title_wrapper.controls=[self._title, self._buttons]

    def _refresh_task_list(self):
        '''Обновление списка задач.'''

        if self._tag.id is None:
            return

        tasks = self._task_service.get_all(self._tag)
        self._task_list.controls = [ft.Text(
            value='Здесь пока ничего нет',
            margin=ft.Margin.only(bottom=10)
        )]
        if len(tasks):
            task_elements = [TaskElement(task) for task in tasks]
            self._task_list.controls = [
                component.build() for component in task_elements
            ]

        self._task_creation_btn = TaskCreationButton(
            self._tag.id,
            self._task_service,
            self._refresh_task_list
        )
        self._task_list.controls.append(self._task_creation_btn.build())
        self._page.update()

    def _switch_tag_handler(self, _):
        '''Обработка открытия и закрытия раздела.'''

        state = not self._tag.is_open

        self._tag.is_open = state
        self._task_tag_service.update(self._tag)

        self._buttons.visible = state

        if not state and (self._is_deleting or self._is_editing):
            self._is_deleting = False
            self._is_editing = False
            self._refresh()

        if state and self._task_creation_btn.is_creating:
            self._task_creation_btn.is_creating = False

    @property
    def _is_deleting(self):
        return self.__is_deleting

    @_is_deleting.setter
    def _is_deleting(self, value: bool):
        '''Обработка режима удаления.'''

        if value and not self._is_deleting:
            self._title.value = 'Вы уверены?'
            self._title.color = ColorPalette.RED

            cancel_btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ColorPalette.MAIN,
                on_click=lambda _: setattr(self, '_is_deleting', False)
            )
            self._buttons.controls = [self._delete_btn, cancel_btn]

        elif value and self._is_deleting:
            self._task_tag_service.delete_tag(self._tag)
            self._refresh_list_callback()

        else:
            self._refresh()

        self.__is_deleting = value

    @property
    def _is_editing(self):
        return self.__is_editing

    @_is_editing.setter
    def _is_editing(self, value: bool):
        '''Обработка режима редактирования.'''

        if value and not self._is_editing:
            self._title_input = ft.TextField(
                hint_text='Новый раздел',
                text_size=16,
                value=self._tag.title,
                autofocus=True,
                border=ft.InputBorder.NONE,
                content_padding=0,
                expand=True
            )

            cancel_btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ColorPalette.MAIN,
                on_click=lambda _: setattr(self, '_is_editing', False)
            )

            self._edit_btn.icon = ft.Icons.CHECK
            self._edit_btn.icon_color = ColorPalette.GREEN

            self._buttons.controls = [cancel_btn, self._edit_btn]
            self._tile_title_wrapper.controls = [
                self._title_input, self._buttons
            ]

        elif value and self._is_editing:
            if self._title_input.value and \
            self._title_input.value != self._tag.title:
                self._tag.title = self._title_input.value
                self._task_tag_service.update(self._tag)

            self.__is_editing = False
            self._refresh()
            return

        else:
            self._refresh()

        self.__is_editing = value
