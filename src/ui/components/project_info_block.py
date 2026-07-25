import flet as ft
from flet.controls.services.url_launcher import UrlLauncher

from ...constants import ColorPalette
from ...models import Project


class ProjectInfoBlock:
    '''Блок информации о проекте для экрана проектов.'''

    def __init__(self, project: Project, page: ft.Page):
        self._page = page
        self._project = project

    def build(self) -> ft.Control:
        '''Построение интерфейса блока.'''

        self._column = ft.Column()
        self.refresh_rows()

        return ft.Container(
            self._column,
            bgcolor='#fff',
            border_radius=10,
            padding=ft.Padding(10, 15, 10, 10),
            alignment=ft.Alignment.TOP_LEFT
        )

    async def _on_phone_tap(self, _):
        '''Обработка нажатия на номер телефона.'''

        url_launcer = ft.UrlLauncher()
        url = f'tel:{self._phone}'

        if await url_launcer.can_launch_url(url):
            await url_launcer.launch_url(url)
        else:
            notif = ft.SnackBar(
                content='Ошибка: звонки не поддерживаются на этом устройстве',
                behavior=ft.SnackBarBehavior.FLOATING,
                bgcolor=ColorPalette.RED
            )

            self._page.show_dialog(notif)

    def _get_row_info(
        self,
        icon: ft.IconData,
        text: str | None,
        icon_color: ft.ColorValue = ColorPalette.MAIN,
        phone_number: bool = False
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

        content = text_widget
        if phone_number:
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
            phone_number=True
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
