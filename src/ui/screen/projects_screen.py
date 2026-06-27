from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

class ProjectsScreen(Screen):
    '''Экран выбора проектов.'''

    projects_list = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
