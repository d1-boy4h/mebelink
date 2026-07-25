from datetime import date, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..constants import ProjectStatus
from ..db.base import Base


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
