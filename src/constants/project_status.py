from enum import StrEnum
from .color_palette import ColorPalette

class ProjectStatus(StrEnum):
    '''Статусы проекта (в работе, не в работе).'''

    NOT_IN_PROGRESS = 'not_in_progress'
    IN_PROGRESS     = 'in_progress'
    POSTPONED       = 'postponed'
    COMPLETED       = 'completed'

    @property
    def ru(self) -> str:
        return {
            ProjectStatus.NOT_IN_PROGRESS: 'Не в работе',
            ProjectStatus.IN_PROGRESS:     'В работе',
            ProjectStatus.POSTPONED:       'Отложен',
            ProjectStatus.COMPLETED:       'Завершён'
        }[self]

    @property
    def color(self) -> str:
        return {
            ProjectStatus.NOT_IN_PROGRESS: ColorPalette.GRAY,
            ProjectStatus.IN_PROGRESS:     ColorPalette.YELLOW,
            ProjectStatus.POSTPONED:       ColorPalette.PURPLE,
            ProjectStatus.COMPLETED:       ColorPalette.GREEN
        }[self]
