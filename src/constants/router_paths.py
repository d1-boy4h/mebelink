from enum import StrEnum


class RouterPaths(StrEnum):
    '''Пути для экранов.'''

    HOME             = '/'
    SETTINGS         = '/settings'
    PROJECT          = '/project'
    PROJECT_CREATION = '/project-creation'
    PROJECT_SETTINGS = '/project-settings'
