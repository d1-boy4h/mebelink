from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Manifest(BaseModel):
    '''Pydantic-модель манифеста mblp-файла.'''

    format_version: int
    project_uuid: UUID
    project_title: str
    exported_at: datetime
