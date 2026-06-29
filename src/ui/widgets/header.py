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

        with self.canvas.before: # type: ignore
            Color(rgb=hex(ColorPalette.MAIN))
            self._bg = Rectangle()
            self.bind(size=self._update_bg, pos=self._update_bg)

        self.logo = Label(
            text='MebeLink',
            bold=True,
            color=hex(ColorPalette.WHITE),
            font_size=sp(32),
            size_hint=(None, None)
        )

        self.logo.bind(texture_size=self._update_size)

        self.add_widget(self.logo)

    def _update_bg(self, *args):
        '''Выравнивание размера фона по размеру виджета.'''
        self._bg.size = self.size
        self._bg.pos = self.pos

    def _update_size(self, *args):
        '''Выравнивание размера виджета по текстуре текста.'''
        self.logo.size = self.logo.texture_size
        self.height = self.logo.height + self.padding[1] * 2 # type: ignore
