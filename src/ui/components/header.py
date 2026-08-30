from collections.abc import Callable
from typing import Literal

import flet as ft

from ...constants import ColorPalette


class Header:
    '''Шапка приложения.'''

    def __init__(
        self,
        title: str,
        font_size: int = 24,
        weight: Literal['normal', 'bold'] = 'normal',
        on_back: Callable | None = None
    ):
        self.__title = title
        self._weight = None if weight == 'normal' else ft.FontWeight.BOLD
        self._font_size = font_size
        self._on_back = on_back

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, text: str):
        self.__title = text
        self._header_title.value = text

    def build(self) -> ft.Control:
        '''Сборка интерфейса шапки.'''

        self._header_title = ft.Text(
            value=self.title,
            color='#fff',
            size=self._font_size,
            weight=self._weight,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            expand=True
        )

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color='#fff',
            on_click=self._on_back
        )

        header_content = ft.Row([self._header_title])

        if self._on_back is not None:
            header_content.controls = [back_button] + header_content.controls

        header = ft.Container(
            header_content,
            bgcolor=ColorPalette.MAIN,
            width=float('inf'),
            padding=ft.Padding(20, 15, 20, 10)
        )

        return header
