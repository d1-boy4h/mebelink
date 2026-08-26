from pydantic import BaseModel


class TaskTag(BaseModel):
    '''Pydantic-модель раздела для задач.'''

    id: int | None = None
    title: str
    is_open: bool = True
