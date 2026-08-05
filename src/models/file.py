from datetime import datetime

from pydantic import BaseModel, Field


class File(BaseModel):
    '''Pydantic-модель файла внутри проекта.'''

    id: int
    filename: str
    path: str
    uploaded_date: datetime = Field(default_factory=datetime.now)
