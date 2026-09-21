from collections.abc import Callable

import flet as ft

from .....constants import ColorPalette, ProjectStatus
from .....models import Project


class ProjectElement:
    '''Элемент списка проектов для домашнего экрана.'''

    def __init__(self, project: Project):
        self._project = project

    def build(self, on_click: Callable[[Project], None]) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        name = ft.Text(
            value=self._project.title,
            size=20,
            color='#000',
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            expand=True
        )

        status = ft.Icon(
            ft.Icons.CONSTRUCTION, self._project.status.color, 16,
            visible=self._project.status != ProjectStatus.NOT_IN_PROGRESS
        )

        improvements = ft.Icon(
            ft.Icons.BUILD, ColorPalette.RED, 14,
            visible=self._project.is_improvements
        )

        project_title = ft.Row([status, improvements, name], spacing=5)

        start_date_str = self._project.start_date.strftime('%d.%m.%y')
        end_date_str = '-'

        if self._project.end_date:
            end_date_str = self._project.end_date.strftime('%d.%m.%y')

        project_date_str = ft.Text(
            value=f'{start_date_str} / {end_date_str}',
            color=ColorPalette.BRIGHT_TEXT
        )

        project_date_icon = ft.Icon(ft.Icons.DATE_RANGE, ColorPalette.MAIN, 14)
        project_date = ft.Row(
            [project_date_icon, project_date_str],
            spacing=5
        )

        project_content = ft.Column(
            controls=[project_title, project_date],
            spacing=0
        )

        project_element = ft.Button(
            project_content,
            on_click=lambda _: on_click(self._project),
            style=ft.ButtonStyle(
                bgcolor='#fff',
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(20, 15, 20, 10),
                alignment=ft.Alignment.TOP_LEFT
            )
        )

        return ft.Container(project_element, margin=ft.Margin(20, 0, 20))
