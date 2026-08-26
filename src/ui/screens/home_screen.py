import flet as ft

from ...constants import ColorPalette, RouterPaths
from ...models import Project
from ...services import ProjectService
from ..components import Header, ProjectElement
from ..store import store
from .base_screen import BaseScreen


class HomeScreen(BaseScreen):
    '''Домашний экран со списком проектов.'''

    def __init__(
            self,
            page: ft.Page,
            project_service: ProjectService,
        ):
        super().__init__(page)
        self._project_service = project_service

    def build(self, route: str) -> ft.View:
        '''Сборка интерфейса экрана.'''

        header_component = Header(self._page, self._page.route)
        header = header_component.build()

        self._project_list_content = ft.ListView(
            self._get_projects(),
            spacing=20
        )

        project_list = ft.Container(
            self._project_list_content,
            bgcolor=ColorPalette.BACKGROUND,
            expand=True,
            width=float('inf'),
            padding=ft.Padding.only(top=20, bottom=20)
        )

        wrapper = ft.Column(
            [header, project_list],
            spacing=0
        )

        create_project_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=ColorPalette.MAIN,
            foreground_color='#fff',
            margin=ft.Margin(0, 0, 30, 30),
            right=0,
            bottom=0,
            on_click=self._show_create_project_modal
        )

        screen_content = ft.Stack([wrapper, create_project_button])
        appbar_wrapper = ft.SafeArea(screen_content, expand=True)
        return ft.View([appbar_wrapper], route, padding=0)

    def _get_projects(self) -> list[ft.Control]:
        '''Получение списка проектов.'''

        projects = self._project_service.get_all()

        elements = []
        for project in projects:
            element = ProjectElement(project)
            elements.append(
                element.build(self._go_to_project_screen)
            )

        return elements

    def _show_create_project_modal(self, *args):
        '''Отображение модального окна создания проекта.'''

        self._text_input = ft.TextField(
            hint_text='Новый проект',
            autofocus=True,
            border=ft.InputBorder.NONE,
            text_size=20
        )

        accept_button = ft.Button(
            'создать',
            on_click=lambda e: self._create_project(self._text_input.value),
            color='#fff',
            width=float('inf'),
            style=ft.ButtonStyle(
                bgcolor=ColorPalette.MAIN,
                text_style=ft.TextStyle(size=18),
                padding=ft.Padding(20, 15, 20, 15)
            )
        )

        modal = ft.AlertDialog(
            self._text_input,
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[accept_button],
            bgcolor='#fff'
        )

        self._page.show_dialog(modal)

    def _go_to_project_screen(self, project: Project):
        '''Переход на экран проекта.'''

        store.current_project = project
        self._page.navigate(RouterPaths.PROJECT_SCREEN)

    def update_project_list(self):
        '''Обновление листа проектов.'''

        self._project_list_content.controls.clear()
        self._project_list_content.controls.extend(self._get_projects())

    def _create_project(self, title: str):
        '''Создание проекта в модальном окне.'''

        # Пасхал очка
        valid_title = title.lower().strip()
        if valid_title == 'сова' or valid_title == 'совы':
            pashalka = '\n' * 10 + '🦉 UwU 🦉' + '\n' * 10
            self._page.pop_dialog()
            self._page.show_dialog(ft.SnackBar(
                content=ft.Text(pashalka, align=ft.Alignment.CENTER),
                behavior=ft.SnackBarBehavior.FLOATING,
                bgcolor=ColorPalette.GREEN
            ))
            self._text_input.value = ''
            return

        new_project = self._project_service.create_project(title)
        self._go_to_project_screen(new_project)

        self._text_input.value = ''
        self._page.pop_dialog()
