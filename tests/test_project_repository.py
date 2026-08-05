from pytest import fixture

from src.db import Database
from src.models import Project
from src.repositories import ProjectRepository


@fixture(scope='module')
def repo():
    '''Инициализация базы данных и сессии.'''

    db = Database()
    return ProjectRepository(db.engine)

@fixture(scope='module')
def project():
    '''Создание простого проекта для тестов.'''
    return Project(title='test_project')

def test_save_and_load(repo, project):
    '''Проверка загрузки и выгрузки проекта из базы данных.'''

    repo._save(project)

    loaded_project = repo.get_by_uuid(project.uuid)
    assert project == loaded_project

def test_update(repo, project):
    '''Проверка обновления проекта в базе данных.'''

    project_title = 'updated_test_project'
    project.title = project_title

    updated_project = repo.update(project)
    assert updated_project.title == project_title

def test_delete(repo, project):
    '''Проверка удаления проекта из базы данных.'''

    deleted_project = repo.delete(project.uuid)
    assert deleted_project is not None
    assert repo.get_by_uuid(deleted_project.uuid) is None
