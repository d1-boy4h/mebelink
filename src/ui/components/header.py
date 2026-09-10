from collections.abc import Callable

import flet as ft

from ...constants import ColorPalette


class Header:
    '''Шапка приложения.'''

    def __init__(
        self,
        title: str,
        is_logo: bool = False,
        on_back: Callable | None = None,
        on_settings: Callable | None = None
    ):
        self.__title = title
        self._on_back = on_back
        self._on_settings = on_settings

        self._is_logo = is_logo
        self._weight = ft.FontWeight.BOLD if is_logo else None
        self._font_size = 32 if is_logo else 24

        self._version = '1.0.3'

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

        settings_button = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_color='#fff',
            on_click=self._on_settings
        )

        header_content = ft.Row([self._header_title])

        if self._on_back is not None:
            header_content.controls = [back_button] + header_content.controls

        if self._on_settings is not None:
            header_content.controls.append(settings_button)

        if self._is_logo:
            version = ft.Text(
                f'v{self._version}',
                color='#ffffff',
                opacity=0.5
            )
            header_content.controls.append(version)

        header = ft.Container(
            header_content,
            bgcolor=ColorPalette.MAIN,
            width=float('inf'),
            padding=ft.Padding(20, 15, 20, 10)
        )

        return header
