import logging
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import Note, NoteDB


class NoteRepository:
    '''Репозиторий заметок проекта.'''

    def __init__(self, engine: Engine):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)

    def _to_orm(self, note: Note) -> NoteDB:
        '''Преобразование модели из Pydantic в ORM.'''

        return NoteDB(
            title=note.title,
            project_uuid=str(note.project_uuid),
            desc=note.desc,
            is_open=note.is_open
        )

    def _to_pydantic(self, note_db: NoteDB) -> Note:
        '''Преобразование модели из ORM в Pydantic.'''

        return Note(
            id=note_db.id,
            title=note_db.title,
            project_uuid=UUID(note_db.project_uuid),
            desc=note_db.desc,
            is_open=note_db.is_open
        )

    def save(self, note: Note) -> Note:
        '''Сохранение заметки в базе данных.'''

        note_db = self._to_orm(note)

        with Session(self._engine) as session:
            session.add(note_db)

            try:
                session.commit()
                session.refresh(note_db)

                self._logger.info(
                    f'Заметка \'{note.title}\' сохранена в базу данных'
                )

                return self._to_pydantic(note_db)

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка сохранения заметки \'{note.title}\': {e}'
                )

                self._logger.error(error)
                raise error

    def get_by_id(self, note_id: int) -> Note | None:
        '''Получение заметки идентификатору.'''

        with Session(self._engine) as session:
            note_db = session.get(NoteDB, note_id)

            if note_db:
                self._logger.info(
                    f'Заметка \'{note_db.title}\' получена из базы данных'
                )
                return self._to_pydantic(note_db)

            return None

    def get_by_project(self, project_uuid: UUID) -> list[Note]:
        '''Получение всех заметок проекта.'''

        with Session(self._engine) as session:
            notes_db = session.execute(
                select(NoteDB).where(NoteDB.project_uuid == str(project_uuid))
            ).scalars().all()

            if len(notes_db):
                self._logger.info(
                    f'Заметок получено из базы данных: {len(notes_db)}'
                )

            return [self._to_pydantic(tag) for tag in notes_db]

    def update(self, note: Note) -> Note:
        '''Обновление данных заметки.'''

        with Session(self._engine) as session:
            note_db = session.get(NoteDB, note.id)

            if not note_db:
                e = ValueError(f'Заметка \'{note.title}\' не найдена')

                self._logger.error(e)
                raise e

            note_db.title = note.title
            note_db.project_uuid = str(note.project_uuid)
            note_db.desc = note.desc
            note_db.is_open=note.is_open

            try:
                session.commit()
                self._logger.info(f'Заметка \'{note.title}\' обновлён')

                return self._to_pydantic(note_db)

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка обновления заметки \'{note.title}\': {e}'
                )

                self._logger.error(error)
                raise error

    def delete(self, note_id: int) -> Note | None:
        '''Удаление раздела.'''

        with Session(self._engine) as session:
            note_db = session.get(NoteDB, note_id)
            if not note_db: return None

            deleted_note = self._to_pydantic(note_db)

            session.delete(note_db)

            try:
                session.commit()
                self._logger.info(f'Заметка \'{deleted_note.title}\' удалена')

                return deleted_note

            except SQLAlchemyError as e:
                session.rollback()
                error = RuntimeError(
                    f'Ошибка удаления заметки \'{note_db.title}\': {e}'
                )

                self._logger.error(error)
                raise error
