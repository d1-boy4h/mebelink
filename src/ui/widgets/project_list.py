# pyright: reportAttributeAccessIssue=false

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import dp

from ...models import Project
from ...constants import ColorPalette
from .project_list_element import ProjectListElement

class ProjectList(ScrollView):
    '''Список проектов.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.do_scroll_x = False

        self.bind(size=self._make_bg)

        self.wrapper = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            padding=(0, dp(5), 0, 0),
        )

        self.wrapper.bind(size=self._do_correct_height)
        self.add_widget(self.wrapper)

    def _make_bg(self, *args):
        '''Создание фона.'''
        with self.canvas.before:
            Color(rgb=hex(ColorPalette.BACKGROUND))
            Rectangle(size=self.size, pos=self.pos)

    def _do_correct_height(self, instance, *args):
        '''Выравнивание высоты по количеству элементов.'''
        instance.height = instance.minimum_height

    def create_elements(self, projects_list: list[Project]):
        '''Заполнение списка проектами.'''
        self.wrapper.clear_widgets()

        for project in projects_list:
            self.wrapper.add_widget(
                ProjectListElement(project.title)
            )
