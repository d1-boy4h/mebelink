from pydantic import BaseModel, field_validator
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Task(BaseModel):
    '''Pydantic-модель задачи внутри проекта.'''

    id: int | None = None
    task_tag_id: int
    title: str
    is_completed: bool = False

    @field_validator('title')
    @classmethod
    def set_title(cls, v: str) -> str:
        if not v:
            return 'Новая задача'

        return v.strip()

class TaskDB(Base):
    '''ORM-модель задачи внутри проекта.'''

    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_tag_id: Mapped[int] = mapped_column(
        ForeignKey('task_tags.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    is_completed: bool = False
