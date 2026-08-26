from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class TaskTagDB(Base):
    '''ORM-модель раздела для задач.'''

    __tablename__ = 'task_tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    is_open: bool = True
