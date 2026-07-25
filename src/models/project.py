from uuid import UUID, uuid4
from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from ..constants import ProjectStatus

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

    @field_validator('title')
    @classmethod
    def set_title(cls, v: str) -> str:
        if not v:
            return 'Новый проект'

        return v.strip()

    @field_validator('start_date')
    @classmethod
    def set_start_date(cls, v: date, info) -> date:
        if v is None:
            created_date: datetime = info.adte.get('created_date')
            return created_date.date()

        return v
