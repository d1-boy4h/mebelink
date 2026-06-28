from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

from ...models import Project
from ..widgets import Header, ProjectList, CreateProjectButton

class ProjectScreen(Screen):
    '''Экран выбора проектов.'''

    def __init__(self, projects: list[Project], **kwargs):
        super().__init__(**kwargs)

        header = Header()
        project_list = ProjectList()

        container = BoxLayout(orientation='vertical')
        container.add_widget(header)
        container.add_widget(project_list)
        project_list.create_elements(projects)
        self.add_widget(container)

        create_project_button = CreateProjectButton()
        create_project_button_wrapper = AnchorLayout(
            anchor_x='right',
            anchor_y='bottom',
            padding=(0, 0, dp(10), dp(10))
        )
        create_project_button_wrapper.add_widget(create_project_button)
        self.add_widget(create_project_button_wrapper)
