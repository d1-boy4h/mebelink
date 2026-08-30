from uuid import UUID

from ..models import Note
from ..repositories import NoteRepository


class NoteService:
    '''Сервис работы с заметками проектов.'''

    def __init__(self, note_repo: NoteRepository):
        self._note_repo = note_repo

    def create(self, title: str, project_uuid: UUID) -> Note:
        '''Создание заметки.'''

        return self._note_repo.save(Note(
            title=title, project_uuid=project_uuid
        ))

    def get_all(self, project_uuid: UUID) -> list[Note]:
        '''Получение всех заметок проекта.'''
        return self._note_repo.get_by_project(project_uuid)

    def update(self, note: Note) -> Note:
        '''Обновление данных заметки.'''
        return self._note_repo.update(note)

    def delete(self, note: Note) -> Note | None:
        '''Удаление заметки.'''

        if note.id is None:
            return None

        return self._note_repo.delete(note.id)

    def delete_project_notes(self, project_uuid: UUID) -> list[Note]:
        '''Удаление всех заметок проекта.'''

        notes = self._note_repo.get_by_project(project_uuid)
        deleted_notes = []
        for note in notes:
            if note.id is not None:
                deleted_note = self._note_repo.delete(note.id)
                if isinstance(deleted_note, Note):
                    deleted_notes.append(deleted_note)

        return deleted_notes
