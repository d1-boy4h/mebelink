from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from ..constants import ProjectStatus

class Project(BaseModel):
    '''Pydantic-модель мебельного проекта.'''

    uuid: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=3)
    status: ProjectStatus = ProjectStatus.NOT_IN_PROGRESS
    is_improvements: bool = False
    created_date: datetime = Field(default_factory=datetime.now)
    start_date: datetime | None = None
    end_date: datetime | None = None
