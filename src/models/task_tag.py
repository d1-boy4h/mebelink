from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class TaskTag(BaseModel):
    '''Pydantic-модель раздела для задач.'''

    id: int | None = None
    title: str
    is_open: bool = True

class TaskTagDB(Base):
    '''ORM-модель раздела для задач.'''

    __tablename__ = 'task_tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    is_open: bool = True
