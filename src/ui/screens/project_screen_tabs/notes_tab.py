import flet as ft

from ....constants import ColorPalette
from ....services import NoteService
from ...components import NoteElement
from ...store import store


class NotesTab:
    '''Вкладка с заметками проекта.'''

    def __init__( self, page: ft.Page, note_service: NoteService):
        self._page = page
        self._note_service = note_service

    def build(self) -> ft.Control:
        '''Сборка интерфейса вкладки.'''

        self._project = store.current_project
        if self._project is None:
            raise RuntimeError('Такого проекта не существует')

        self._notes_listview = ft.ListView(
            controls=[],
            spacing=20,
            padding=ft.Padding(20, 0, 20, 20)
        )

        create_note_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=ColorPalette.MAIN,
            foreground_color='#fff',
            margin=ft.Margin(0, 0, 30, 30),
            right=0,
            bottom=0,
            on_click=self._show_create_note_modal
        )

        self.refresh()

        return ft.Stack([self._notes_listview, create_note_button])

    def refresh(self):
        '''Обновление списка разделов задач.'''

        if self._project is None:
            return

        notes = self._note_service.get_all(self._project.uuid)
        store.current_notes = notes[:]

        note_elements = []
        for note in notes:
            note_element = NoteElement(
                note,
                self._page,
                self._note_service,
                self.refresh
            )
            note_elements.append(note_element.build())

        self._notes_listview.controls = note_elements
        self._page.update()

    def _show_create_note_modal(self, _):
        '''Отображение модального окна создания заметки.'''

        self._text_input = ft.TextField(
            hint_text='Новая заметка',
            autofocus=True,
            border=ft.InputBorder.NONE,
            text_size=20
        )

        accept_button = ft.Button(
            'создать',
            on_click=lambda _: self._create_note(self._text_input.value),
            color='#fff',
            width=float('inf'),
            style=ft.ButtonStyle(
                bgcolor=ColorPalette.MAIN,
                text_style=ft.TextStyle(size=18),
                padding=ft.Padding(20, 15, 20, 15)
            )
        )

        modal = ft.AlertDialog(
            self._text_input,
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[accept_button],
            bgcolor='#fff'
        )

        self._page.show_dialog(modal)

    def _create_note(self, title: str):
        '''Создание заметки в модальном окне.'''

        if self._project is None:
            return

        self._note_service.create(title, self._project.uuid)

        self.refresh()
        self._page.pop_dialog()
        self._page.update()
