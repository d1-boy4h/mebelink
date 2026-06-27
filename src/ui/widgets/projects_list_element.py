from kivy.uix.button import Button
from kivy.properties import StringProperty

class ProjectsListElement(Button):
    '''Элемент списка проектов.'''

    project_title = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
