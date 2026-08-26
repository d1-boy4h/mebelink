from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..constants import ProjectStatus
from ..db import Base


class Project(BaseModel):
    '''Pydantic-модель мебельного проекта.'''

    uuid: UUID = Field(default_factory=uuid4)
    title: str
    status: ProjectStatus = ProjectStatus.NOT_IN_PROGRESS
    is_improvements: bool = False
    created_date: datetime = Field(default_factory=datetime.now)
    start_date: date = Field(default_factory=date.today)
    end_date: date | None = None
    address: str | None = None
    phone: str | None = None

    @field_validator('title')
    @classmethod
    def set_title(cls, v: str) -> str:
        if not v:
            return 'Новый проект'

        return v.strip()

class ProjectDB(Base):
    '''ORM-модель мебельного проекта.'''

    __tablename__ = 'projects'

    uuid: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        nullable=False
    )

    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(String(16), nullable=False)
    is_improvements: Mapped[bool] = mapped_column(nullable=False)
    created_date: Mapped[datetime] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date | None]
    address: Mapped[str | None]
    phone: Mapped[str | None]
