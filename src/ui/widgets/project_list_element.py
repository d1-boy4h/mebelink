# pyright: reportAttributeAccessIssue=false

from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as hex

from ...constants import ColorPalette

class ProjectListElement(Button):
    '''Элемент списка проектов.'''

    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)

        self.text = title
        self.shorten = True
        self.shorten_from = 'right'
        self.font_size = sp(20)
        self.color = hex(ColorPalette.BLACK)

        self.background_down = ''
        self.background_normal = ''
        self.background_color = hex(ColorPalette.WHITE)

        self.size_hint_y = None
        
        self.bind(
            texture_size=self._update_button_size,
            size=self._update_text_size,
            state=self._change_bg,
        )

        self.padding = (dp(10), dp(20), dp(10), dp(10))

    def _update_button_size(self, *args):
        '''Выравнивание размеров кнопки по текстуре текста.'''
        self.height = self.texture_size[1]

    def _update_text_size(self, *args):
        '''Выравнивание области текста по размеру кнопки.'''
        self.text_size = self.size

    def _change_bg(self, *args):
        '''Изменение фона при нажатии на элемент.'''
        if self.state == 'down':
            self.background_color = hex(ColorPalette.BUTTON_DOWN)
        else:
            self.background_color = hex(ColorPalette.WHITE)
