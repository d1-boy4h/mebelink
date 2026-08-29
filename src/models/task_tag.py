from uuid import UUID

from pydantic import BaseModel, field_validator
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class TaskTag(BaseModel):
    '''Pydantic-модель раздела для задач.'''

    id: int | None = None
    project_uuid: UUID
    title: str
    is_open: bool = True

    @field_validator('title')
    @classmethod
    def set_title(cls, v: str) -> str:
        if not v:
            return 'Новый раздел'

        return v.strip()

class TaskTagDB(Base):
    '''ORM-модель раздела для задач.'''

    __tablename__ = 'task_tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('projects.uuid', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    is_open: Mapped[bool]
