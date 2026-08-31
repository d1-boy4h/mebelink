import asyncio
from collections.abc import Callable

import flet as ft

from ...constants import ColorPalette
from ...models import Note
from ...services import NoteService


class NoteElement:
    '''Элемент заметки (раскрывающийся).'''

    def __init__(
        self,
        note: Note,
        page: ft.Page,
        note_service: NoteService,
        refresh_list_callback: Callable
    ):
        self._note = note

        self._page = page
        self._note_service = note_service
        self._refresh_list_callback = refresh_list_callback

        self.__is_deleting: bool = False
        self.__is_editing: bool = False
        self._save_task: asyncio.Task | None = None

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        self._title = ft.Text(self._note.title, expand=True)

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
            visible=self._note.is_open
        )

        self._tile_title_wrapper = ft.Row(
            controls=[self._title, self._buttons],
            spacing=0
        )

        self._description = ft.TextField(
            text_size=16,
            hint_text='Описание',
            value=self._note.desc,
            autofocus=True,
            multiline=True,
            expand=True,
            on_blur=self._save_desc_note,
            on_change=self._on_desc_change,
            content_padding=ft.Padding.all(0),
            border=ft.InputBorder.NONE
        )

        return ft.ExpansionTile(
            title=self._tile_title_wrapper,
            controls=[self._description],
            bgcolor='#fff',
            collapsed_bgcolor='#fff',
            shape=ft.RoundedRectangleBorder(radius=10),
            collapsed_shape=ft.RoundedRectangleBorder(radius=10),
            controls_padding=ft.Padding(20, 15, 20, 10),
            on_change=self._switch_note_handler,
            expanded=self._note.is_open
        )

    def _refresh(self):
        '''Сброс компонента по умолчанию.'''

        self._title.value = self._note.title
        self._title.color = None

        self._edit_btn.icon = ft.Icons.EDIT
        self._edit_btn.icon_color = ColorPalette.MAIN

        self._buttons.controls = [self._edit_btn, self._delete_btn]
        self._tile_title_wrapper.controls=[self._title, self._buttons]

    def _switch_note_handler(self, _):
        '''Обработка открытия и закрытия заметки.'''

        state = not self._note.is_open

        self._note.is_open = state
        self._note_service.update(self._note)

        self._buttons.visible = state

        if not state and (self._is_deleting or self._is_editing):
            self._is_deleting = False
            self._is_editing = False
            self._refresh()

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
            self._note_service.delete(self._note)
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
                hint_text=self._note.title,
                text_size=16,
                value=self._note.title,
                autofocus=True,
                multiline=True,
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
            self._title_input.value != self._note.title:
                self._note.title = self._title_input.value
                self._note_service.update(self._note)

            self.__is_editing = False
            self._refresh()
            return

        else:
            self._refresh()

        self.__is_editing = value

    def _on_desc_change(self, _):
        '''Debounce-декоратор для сохранения описания заметки.'''

        if self._save_task:
            self._save_task.cancel()

        self._save_task = asyncio.create_task(self._save_desc_with_delay())
        self._description.color = ColorPalette.GRAY

    async def _save_desc_with_delay(self):
        '''Сохранение заметки через секунду после последнего изменения.'''

        await asyncio.sleep(1)
        self._save_desc_note()

    def _save_desc_note(self, _ = None):
        '''Сохранение описания заметки.'''

        new_desc = self._description.value

        if self._note.desc != new_desc.strip():
            self._note.desc = new_desc
            self._note_service.update(self._note)

        self._save_task = None
        self._description.color = None
        self._page.update()
