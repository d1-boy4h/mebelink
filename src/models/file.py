from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class File(BaseModel):
    '''Pydantic-модель файла внутри проекта.'''

    id: int | None = None
    project_uuid: UUID
    filename: str
    path: str
    uploaded_date: datetime = Field(default_factory=datetime.now)

class FileDB(Base):
    '''ORM-модель файла внутри проекта.'''

    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('projects.uuid', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    filename: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    uploaded_date: Mapped[datetime] = mapped_column(nullable=False)