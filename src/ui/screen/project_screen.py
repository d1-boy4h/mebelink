# pyright: reportAttributeAccessIssue=false

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

from ..widgets import \
    Header, \
    ProjectList, \
    ProjectScreenButton, \
    CreateProjectModal

from ...services import ProjectService

class ProjectScreen(Screen):
    '''Экран выбора проектов.'''

    def __init__(
        self,
        project_service: ProjectService,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.project_service = project_service

        header = Header()
        self.project_list = ProjectList()
        self.project_list.create_elements(
            self.project_service.get_all()
        )

        container = BoxLayout(orientation='vertical')
        container.add_widget(header)
        container.add_widget(self.project_list)

        self.add_widget(container)

        create_project_button_wrapper = AnchorLayout(
            anchor_x='right',
            anchor_y='bottom',
            padding=(0, 0, dp(10), dp(10))
        )
        create_project_button = ProjectScreenButton()
        create_project_button_wrapper.add_widget(create_project_button)

        modal = CreateProjectModal()
        modal.bind(on_dismiss=self._create_project)
        create_project_button.bind(on_press=lambda *args: modal.open())

        self.add_widget(create_project_button_wrapper)

    def _create_project(self, instance, *args):
        if not instance.is_project_creation:
            return

        project_title = instance.input.text
        instance.input.text = ''

        self.project_service.create_project(project_title)

        self.project_list.create_elements(
            self.project_service.get_all()
        )

        instance.is_project_creation = False
