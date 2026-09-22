from pathlib import Path

import flet as ft

from ...constants import ColorPalette, MetaInfo
from ..components import Header
from ..utils import export_logs, show_notify
from .base_screen import BaseScreen


class SettingsScreen(BaseScreen):
    '''Экран настроек.'''

    def __init__(self, page: ft.Page):
        super().__init__(page)

    def build(self, route: str) -> ft.View:
        '''Сборка интерфейса экрана.'''

        header = Header(
            title='Настройки',
            on_back=lambda: self._page.navigate(
                self._page.views[-2].route
            )
        )

        btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.all(20)
        )

        self._export_logs_btn = ft.Button(
            'Сохранить логи в zip-архив',
            color='#fff',
            bgcolor=ColorPalette.MAIN,
            expand=True,
            style=btn_style,
            on_click=self._on_export_logs_btn_click
        )

        elements_list = ft.ListView(
            controls=[self._export_logs_btn],
            spacing=15,
            padding=ft.Padding.all(20),
            expand=True
        )

        version = ft.Text(
            value=f'Текущая версия: {MetaInfo.VERSION}',
            color=ColorPalette.GRAY
        )

        name = ft.Text(
            value='Бойченко И. В.   |   ',
            color=ColorPalette.GRAY
        )

        tg_link_value = ft.Text(
            value='@d1_boy4h',
            color=ColorPalette.MAIN,
            style = ft.TextStyle(
                decoration=ft.TextDecoration.UNDERLINE,
                decoration_color=ColorPalette.MAIN
            )
        )

        tg_link = ft.GestureDetector(
            tg_link_value,
            on_tap=self._on_url_click,
            mouse_cursor=ft.MouseCursor.CLICK
        )

        author = ft.Row([name, tg_link], spacing=0)

        text_block = ft.Column(
            controls=[version, author],
            spacing=0,
            margin=ft.Margin.only(bottom=10, left=15)
        )

        body = ft.Container(
            content=ft.Column([elements_list, text_block], spacing=0),
            bgcolor=ColorPalette.BACKGROUND,
            expand=True,
            width=float('inf')
        )

        screen_content = ft.Column([header.build(), body], spacing=0)
        appbar_wrapper = ft.SafeArea(screen_content, expand=True)
        return ft.View([appbar_wrapper], route, padding=0)

    async def _on_url_click(self, _):
        '''Обработка нажатия на ссылку.'''

        url_launcer = ft.UrlLauncher()
        await url_launcer.launch_url('https://t.me/d1_boy4h')

    async def _on_export_logs_btn_click(self, _):
        '''Обработка нажатия на кнопку экспорта логов.'''

        self._export_logs_btn.disabled = True
        self._export_logs_btn.bgcolor = ColorPalette.GRAY

        try:
            zip_bytes = export_logs()

            file_picker = ft.FilePicker()
            path = await file_picker.save_file(
                dialog_title='Экспорт логов...',
                file_name='logs.zip',
                src_bytes=zip_bytes
            )

            if path is not None:
                if self._page.platform != ft.PagePlatform.ANDROID:
                    Path(path).write_bytes(zip_bytes)

                    show_notify(
                        page=self._page,
                        text=f'Логи успешно сохранены:\n{path}'
                    )

                else:
                    show_notify(self._page, 'Логи успешно сохранены')

        except RuntimeError as error:
            show_notify(self._page, str(error), is_error=True)

        finally:
            self._export_logs_btn.disabled = False
            self._export_logs_btn.bgcolor = ColorPalette.MAIN

        self._page.update()
