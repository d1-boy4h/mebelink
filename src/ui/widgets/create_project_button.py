# pyright: reportAttributeAccessIssue=false

from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import sp, dp
from math import hypot

from ...constants import ColorPalette

class CreateProjectButton(Button):
    '''Кнопка добавления нового проекта.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = '+'
        self.font_size = sp(36)

        self.size_hint = (None, None)
        self.background_down = ''
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        
        self.bind(
            texture_size=self._make_bg,
            pos=self._do_correct_bg_pos,
            state=self._change_bg
        )

    def _make_bg(self, *args):
        '''Создание фона.'''
        area = dp(30)

        with self.canvas.before: # type: ignore
            self.bg_color = Color(rgb=hex(ColorPalette.MAIN))
            self.bg_ellipse = Ellipse(
                size=(
                    self.texture_size[1] + area,
                    self.texture_size[1] + area
                ),
                pos=self.pos
            )

    def _do_correct_bg_pos(self, *args):
        '''Выравнивание позиции фона кнопки по текстуре текста кнопки.'''
        self.bg_ellipse.pos = (
            self.center_x - self.bg_ellipse.size[0] / 2,
            self.center_y - self.bg_ellipse.size[1] / 2,
        )

    def _change_bg(self, *args):
        '''Изменение фона при нажатии на кнопку.'''
        if self.state == 'down':
            self.bg_color.rgb = hex(ColorPalette.BUTTON_DOWN)
        else:
            self.bg_color.rgb = hex(ColorPalette.MAIN)

    def collide_point(self, x, y):
        '''Переопределение метода вычисления области нажатия кнопки.'''
        distance = hypot(x - self.center_x, y - self.center_y)
        radius = self.bg_ellipse.size[0] / 2

        return distance <= radius
