from uuid import UUID

from pydantic import BaseModel, field_validator
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Note(BaseModel):
    '''Pydantic-модель заметки проекта.'''

    id: int | None = None
    project_uuid: UUID
    title: str
    desc: str = ''
    is_open: bool = True

    @field_validator('title')
    @classmethod
    def set_title(cls, v: str) -> str:
        if not v:
            return 'Новая заметка'

        return v.strip()

class NoteDB(Base):
    '''ORM-модель заметки проекта.'''

    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('projects.uuid', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    desc: Mapped[str]
    is_open: Mapped[bool]
