from enum import StrEnum


class ImportConflictAction(StrEnum):
    '''Действие пользователя в случае конфликта импорта проектов.'''

    CANCEL    = 'cancel'
    OVERWRITE = 'overwrite'
    DUPLICATE = 'duplicate'
