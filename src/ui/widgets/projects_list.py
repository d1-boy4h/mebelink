from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from ...models import Project
from .projects_list_element import ProjectsListElement

class ProjectsList(ScrollView):
    '''Список проектов.'''

    projects_list_wrapper = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_elements(self, projects_list: list[Project]):
        self.projects_list_wrapper.clear_widgets()

        for project in projects_list:
            self.projects_list_wrapper.add_widget(
                ProjectsListElement(project_title=project.title)
            )
