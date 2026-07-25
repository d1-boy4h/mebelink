import flet as ft

from ...models import Project
from ...constants import ColorPalette

class ProjectInfoBlock:
    '''Блок информации о проекте для экрана проектов.'''

    def __init__(self, project: Project):
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
    
    def _get_row_info(
        self,
        icon: ft.IconData,
        text: str | None,
        icon_color: ft.ColorValue = ColorPalette.MAIN,
    ) -> ft.Control:
        '''Возвращает строку (ft.Row) информации о проекте.'''

        if text is None:
            return ft.Row(visible=False)

        return ft.Row([
            ft.Icon(icon, icon_color, 20),
            ft.Text(text, expand=True, size=16, style=ft.TextStyle(height=1.1))
        ], spacing=10)

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
            status,
            improvements,
            deadlines,
            created_date
        ]
