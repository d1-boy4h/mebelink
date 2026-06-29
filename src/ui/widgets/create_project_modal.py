# pyright: reportAttributeAccessIssue=false

from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp, sp

from .project_screen_button import ProjectScreenButton

class CreateProjectModal(ModalView):
    '''Модальное окно создания проекта.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_project_creation = False

        self.background_color = (0, 0, 0, 0)

        self.input = TextInput(
            hint_text='Название проекта',
            font_size=sp(20),
            multiline=False,
            background_color=(1, 1, 1, 1),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            width=dp(300),
            padding=(dp(10), dp(20), dp(10), dp(10)),
            cursor_color=(0, 0, 0, 1),
        )

        self.input.bind(minimum_height=self._update_input)
        self.input.bind(text=self._button_status)

        self.button = ProjectScreenButton(disabled=True)
        self.button.bind(on_release=self._on_project_create)

        self.button_wrapper = AnchorLayout(
            anchor_x='right',
            anchor_y='bottom',
            padding=(0, 0, dp(10), dp(10))
        )
        self.button_wrapper.add_widget(self.button)

        self.wrapper = FloatLayout()
        self.wrapper.add_widget(self.input)
        self.wrapper.add_widget(self.button_wrapper)

        self.add_widget(self.wrapper)

    def _update_input(self, *args):
        '''Выравнивание высоты формы ввода по минимальной высоте.'''
        self.input.height = self.input.minimum_height

    def _button_status(self, *args):
        if len(self.input.text) < 3:
            self.button.disabled = True
        else:
            self.button.disabled = False

    def _on_project_create(self, *args):
        self.is_project_creation = True
        self.dismiss()

    def on_touch_down(self, touch):
        if self.button.on_touch_down(touch) or self.input.on_touch_down(touch):
            return True # Заглушка
        res = super().on_touch_down(touch)
        self._touch_started_inside = False

        return res
