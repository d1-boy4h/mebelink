import flet as ft

from ...constants import ColorPalette, RouterPaths
from ...models import Project
from ..utils import show_notify


class InfoBlock:
    '''Блок информации о проекте для экрана проектов.'''

    def __init__(self, project: Project, page: ft.Page):
        self._page = page
        self._project = project

    def build(self) -> ft.Control:
        '''Построение интерфейса блока.'''

        self._column = ft.Column()
        self.refresh_rows()

        return ft.Button(
            self._column,
            bgcolor='#fff',
            color='#000',
            elevation=2,
            on_click=lambda: self._page.navigate(
                RouterPaths.PROJECT_SETTINGS
            ),
            style=ft.ButtonStyle(
                padding=ft.Padding(10, 25, 10, 20),
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.NORMAL
                )
            )
        )

    async def _on_phone_tap(self, _):
        '''Обработка нажатия на номер телефона.'''

        url_launcer = ft.UrlLauncher()
        url = f'tel:{self._phone}'

        if await url_launcer.can_launch_url(url):
            await url_launcer.launch_url(url)
        else:
            show_notify(
                self._page,
                'Звонки не поддерживаются на этом устройстве',
                is_error=True
            )

    def _get_row_info(
        self,
        icon: ft.IconData,
        text: str | None,
        icon_color: ft.ColorValue = ColorPalette.MAIN,
        is_phone_number: bool = False
    ) -> ft.Control:
        '''Возвращает строку (ft.Row) информации о проекте.'''

        if text is None:
            return ft.Row(visible=False)

        text_widget = ft.Text(
            text,
            expand=True,
            size=16,
            style=ft.TextStyle(height=1.1)
        )

        content: ft.Control = text_widget
        if is_phone_number and text.startswith('+') and len(text) >= 12:
            text_widget.color = ColorPalette.MAIN
            text_widget.style = ft.TextStyle(
                height=1.1,
                decoration=ft.TextDecoration.UNDERLINE,
                decoration_color=ColorPalette.MAIN
            )

            self._phone = text
            content = ft.GestureDetector(
                text_widget,
                on_tap=self._on_phone_tap,
                mouse_cursor=ft.MouseCursor.CLICK
            )

        return ft.Row([ft.Icon(icon, icon_color, 20), content], spacing=10)

    def refresh_rows(self):
        '''Обновление информации.'''

        title = self._get_row_info(ft.Icons.TITLE, self._project.title)

        created_date = self._get_row_info(
            ft.Icons.ACCESS_TIME,
            self._project.created_date.strftime('%d.%m.%y %H:%M')
        )

        address = self._get_row_info(
            ft.Icons.LOCATION_ON,
            self._project.address
        )

        phone = self._get_row_info(
            ft.Icons.PHONE,
            self._project.phone,
            is_phone_number=True
        )

        status = self._get_row_info(
            ft.Icons.CONSTRUCTION,
            self._project.status.ru,
            self._project.status.color
        )

        improvements_text = None
        if self._project.is_improvements:
            improvements_text = 'Есть доделки'

        improvements = self._get_row_info(
            ft.Icons.BUILD,
            improvements_text,
            ColorPalette.RED
        )

        first_date = self._project.start_date.strftime('%d.%m.%y')
        second_date = '-'
        if self._project.end_date:
            second_date = self._project.end_date.strftime('%d.%m.%y')

        deadlines = self._get_row_info(
            ft.Icons.DATE_RANGE,
            f'{first_date} / {second_date}'
        )

        self._column.controls = [
            title,
            address,
            phone,
            status,
            improvements,
            deadlines,
            created_date
        ]
