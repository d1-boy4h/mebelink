from kivy.uix.filechooser import Screen
# pyright: reportAttributeAccessIssue=false

from os import environ

environ['KIVY_NO_ARGS'] = 'true'
environ['KIVY_LOG_MODE'] = 'PYTHON'

from kivy.config import Config

Config.set('graphics', 'width', 420)
Config.set('graphics', 'height', 720)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from ..services import ProjectService

class Interface(App):
    '''Корневой класс интерфейса.'''

    title = 'MebeLink: Управление мебельными заказами'
    root: ScreenManager

    def __init__(self, project_service: ProjectService):
        super().__init__()
        self._project_service = project_service
        self._projects = self._project_service.get_all()

    def build(self):
        return Builder.load_file('src/ui/ui.kv')

    def on_start(self):
        self.update_ptoject_list()

    def update_ptoject_list(self):
        project_screen = self.root.get_screen('projects_screen')
        project_screen.projects_list.create_elements(self._projects)
