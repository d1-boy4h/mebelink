import flet as ft

from ..store import store
from ...constants import ColorPalette, RouterPaths

class Header:
    '''Шапка приложения.'''

    def __init__(self, page: ft.Page, route: str):
        self._page = page
        self._route = route

    def build(self) -> ft.Control:
        '''Сборка интерфейса шапки.'''

        self._header_title = ft.Text(
            value='MebeLink',
            color='#fff',
            size=32,
            weight=ft.FontWeight.BOLD,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        header = ft.Container(
            self._header_title,
            bgcolor=ColorPalette.MAIN,
            width=float('inf'),
            padding=ft.Padding(20, 15, 20, 10)
        )

        if self._route != RouterPaths.HOME_SCREEN:
            self._header_title.weight = None
            self._header_title.size = 24
            self._header_title.expand = True

            back_button = ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color='#fff',
                on_click=self._go_to_home_screen
            )

            if self._route == RouterPaths.PROJECT_SCREEN:
                if store.current_project is None:
                    raise RuntimeError('Такого проекта не существует')

                self._header_title.value = store.current_project.title

                settings_button = ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    icon_color='#fff',
                    on_click=lambda e: self._page.navigate(
                        RouterPaths.PROJECT_SETTINGS_SCREEN
                    )
                )

                header.content = ft.Row([
                    back_button, self._header_title, settings_button
                ])

            if self._route == RouterPaths.PROJECT_SETTINGS_SCREEN:
                back_button.on_click = lambda e: self._page.navigate(
                    RouterPaths.PROJECT_SCREEN
                )

                self._header_title.value = 'Настройки проекта'
                header.content = ft.Row([back_button, self._header_title])

        return header

    def _go_to_home_screen(self, *args):
        '''Переход назад на домашний экран.'''

        store.current_project = None
        self._page.navigate(RouterPaths.HOME_SCREEN)

    def refresh_title(self):
        '''Обновление названия проекта.'''

        if store.current_project is None:
            raise RuntimeError('Такого проекта не существует')

        self._header_title.value = store.current_project.title
