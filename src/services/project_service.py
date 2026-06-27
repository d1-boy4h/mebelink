from ..repositories import ProjectRepository
from ..models import Project

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        '''Сервис с бизнес-логикой для работы с мебельными проектами.'''
        self._repo = repo

    def create_project(self, title: str) -> Project:
        '''Создание проекта с валидацией.'''
        if len(title.strip()) < 3:
            raise ValueError('Название проекта должно содержать минимум 3 символа')

        project = Project(title=title)

        return self._repo.save(project)

    def get_all(self) -> list[Project]:
        '''Получение всех проектов.'''
        return self._repo.get_all()
