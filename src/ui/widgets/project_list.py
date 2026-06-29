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

        with self.canvas.before:
            Color(rgb=hex(ColorPalette.BACKGROUND))
            self._bg = Rectangle()
            self.bind(size=self._update_bg)

        self.wrapper = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            padding=(0, dp(5), 0, 0),
            size_hint_y=None
        )

        self.wrapper.bind(minimum_height=self._update_height)
        self.add_widget(self.wrapper)

    def _update_bg(self, *args):
        '''Выравнивание размера фона по размеру виджета.'''
        self._bg.size = self.size
        self._bg.pos = self.pos

    def _update_height(self, *args):
        '''Выравнивание высоты контейнера по количетсву проектов в списке.'''
        self.wrapper.height = self.wrapper.minimum_height

    def create_elements(self, projects_list: list[Project]):
        '''Заполнение списка проектами.'''
        self.wrapper.clear_widgets()

        for project in projects_list:
            element = ProjectListElement(project.title)
            self.wrapper.add_widget(element)
            element.texture_update()
