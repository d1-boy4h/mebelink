# pyright: reportAttributeAccessIssue=false

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import dp, sp

from ...constants import ColorPalette

class Header(BoxLayout):
    '''Шапка для ProjectsScreen.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.padding = dp(10)

        self.bind(size=self._make_bg)

        logo = Label(
            text='MebeLink',
            bold=True,
            color=hex(ColorPalette.WHITE),
            font_size=sp(32),
            size_hint=(None, None)
        )

        logo.bind(texture_size=self._do_correct_size)

        self.add_widget(logo)

    def _make_bg(self, *args):
        '''Создание фона.'''
        with self.canvas.before: # type: ignore
            Color(rgb=hex(ColorPalette.MAIN))
            Rectangle(size=self.size, pos=self.pos)

    def _do_correct_size(self, instance, *args):
        '''Выравнивание размеров по текстуре логотипа.'''
        instance.size = instance.texture_size
        self.height = instance.height + self.padding[1] * 2 # type: ignore
