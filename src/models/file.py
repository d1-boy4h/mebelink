from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class File(BaseModel):
    '''Pydantic-модель файла внутри проекта.'''

    id: int | None = None
    project_uuid: UUID
    filename: str
    path: str
    uploaded_date: datetime = Field(default_factory=datetime.now)
