# pyright: reportAttributeAccessIssue=false

from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import sp, dp
from math import hypot

from ...constants import ColorPalette

class ProjectScreenButton(Button):
    '''Кнопка добавления нового проекта.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = '+'
        self.font_size = sp(36)

        self.size_hint = (None, None)
        self.background_down = ''
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before: # type: ignore
            self._bg_color = Color(rgb=hex(ColorPalette.MAIN))
            self._bg_ellipse = Ellipse()
            self.bind(pos=self._update_bg)

        self.bind(state=self._change_bg)

    def _update_bg(self, *args):
        '''Выравнивание размера фона по текстуре текста.'''
        bg_padding = dp(20)

        self._bg_ellipse.size = (
            self.texture_size[1] + bg_padding,
            self.texture_size[1] + bg_padding
        )

        self._bg_ellipse.pos = (
            self.center_x - self._bg_ellipse.size[0] / 2,
            self.center_y - self._bg_ellipse.size[1] / 2,
        )

    def _change_bg(self, *args):
        '''Изменение фона при нажатии на кнопку.'''
        if self.state == 'down':
            self._bg_color.rgb = hex(ColorPalette.BUTTON_DOWN)
        else:
            self._bg_color.rgb = hex(ColorPalette.MAIN)

    def collide_point(self, x, y):
        '''Переопределение метода вычисления области нажатия кнопки.'''
        distance = hypot(x - self.center_x, y - self.center_y)
        radius = self._bg_ellipse.size[0] / 2

        return distance <= radius
