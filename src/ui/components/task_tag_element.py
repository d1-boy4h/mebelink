from collections.abc import Callable

import flet as ft

from ...constants import ColorPalette
from ...models import TaskTag
from ...services import TaskTagService


class TaskTagElement:
    '''Элемент выпадающего списка (раздела) с задачми проекта.'''

    def __init__(
            self,
            tag: TaskTag,
            task_tag_service: TaskTagService,
            refresh_list_callback: Callable,
            show_edit_tag_modal_callback: Callable[[TaskTag], None]
        ):
        self._tag = tag
        self._task_tag_service = task_tag_service
        self._refresh_list_callback = refresh_list_callback
        self._show_edit_tag_modal_callback = show_edit_tag_modal_callback

        self.__is_deleting: bool = False

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
                on_click=lambda _: setattr(self, '_is_deleting', False)
            )
            self._buttons.controls = [cancel_btn, self._delete_btn]

        elif value and self._is_deleting and self._tag.id is not None:
            self._task_tag_service.delete_tag(self._tag.id)
            self._refresh_list_callback()

        else:
            self._refresh()

        self.__is_deleting = value

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        self._title = ft.Text(self._tag.title, expand=True)

        self._edit_btn = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ColorPalette.MAIN,
            visible=self._tag.is_open,
            on_click=lambda _: self._show_edit_tag_modal_callback(self._tag)
        )

        self._delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ColorPalette.RED,
            visible=self._tag.is_open,
            on_click=lambda _: setattr(self, '_is_deleting', True)
        )

        self._buttons = ft.Row([self._edit_btn, self._delete_btn], spacing=0)
        self._tile_title_wrapper = ft.Row(
            controls=[self._title, self._buttons],
            spacing=0
        )

        return ft.ExpansionTile(
            title=self._tile_title_wrapper,
            controls=[ft.Text('Пока тут ничего нет')],
            bgcolor='#fff',
            collapsed_bgcolor='#fff',
            shape=ft.RoundedRectangleBorder(radius=10),
            collapsed_shape=ft.RoundedRectangleBorder(radius=10),
            controls_padding=ft.Padding(20, 15, 20, 10),
            on_change=self._switch_tag_handler,
            expanded=self._tag.is_open
        )

    def _refresh(self):
        '''Сборс компонента по умолчанию.'''

        self._title.value = self._tag.title
        self._title.color = None
        self._buttons.controls = [self._edit_btn, self._delete_btn]

    def _switch_tag_handler(self, _):
        '''Обработка открытия и закрытия раздела.'''

        state = not self._tag.is_open

        self._tag.is_open = state
        self._task_tag_service.update(self._tag)

        self._edit_btn.visible = state
        self._delete_btn.visible = state

        if not state and self._is_deleting:
            self._is_deleting = False
            self._refresh()
