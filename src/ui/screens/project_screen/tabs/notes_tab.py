import flet as ft

from .....services import NoteService
from ....store import store
from ..components import NoteCreationButton, NoteElement


class NotesTab:
    '''Вкладка с заметками проекта.'''

    def __init__(self, page: ft.Page, note_service: NoteService):
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

        self.refresh()
        return self._notes_listview

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

        self._note_creation_btn = NoteCreationButton(
            self._note_service,
            self.refresh
        )
        note_elements.append(self._note_creation_btn.build())
        self._notes_listview.controls = note_elements
        self._page.update()
