# pyright: reportAttributeAccessIssue=false

from os import environ

environ['KIVY_NO_ARGS'] = 'true'
environ['KIVY_LOG_MODE'] = 'PYTHON'

from kivy.config import Config

Config.set('graphics', 'width', 420)
Config.set('graphics', 'height', 720)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ..services import ProjectService
from .screen import ProjectScreen

class Interface(App):
    '''Корневой класс интерфейса.'''

    title = 'MebeLink: Управление мебельными заказами'

    def __init__(self, project_service: ProjectService):
        super().__init__()

        self._project_service = project_service
        self._projects = self._project_service.get_all()

        self._screen_manager = ScreenManager()
        self._screen_manager.add_widget(
            ProjectScreen(self._projects, name='project_screen')
        )

    def build(self):
        return self._screen_manager
