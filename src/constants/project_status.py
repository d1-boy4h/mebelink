from enum import StrEnum

class ProjectStatus(StrEnum):
    '''Статусы проекта (в работе, не в работе).'''

    IN_PROGRESS     = 'in_progress'
    NOT_IN_PROGRESS = 'not_in_progress'
    POSTPONED       = 'postponed'
    COMPLETED       = 'completed'

    @property
    def ru(self) -> str:
        return {
            ProjectStatus.IN_PROGRESS:     'В работе',    # Жёлтый
            ProjectStatus.NOT_IN_PROGRESS: 'Не в работе', # Без цвета
            ProjectStatus.POSTPONED:       'Отложен',     # Фиолетовый
            ProjectStatus.COMPLETED:       'Завершён'     # Зелёный
        }[self]
