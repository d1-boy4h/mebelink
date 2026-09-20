import flet as ft

from ....constants import ColorPalette, RouterPaths
from ....models import Project
from ....services import ProjectService
from ...components import Header
from ...store import store
from ..base_screen import BaseScreen
from .components import ProjectElement


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

        to_settings_screen_btn = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_color='#fff',
            on_click=lambda: self._page.navigate(
                RouterPaths.SETTINGS
            )
        )

        header = Header(
            'МебеЛинк',
            is_logo=True,
            extra_buttons=[to_settings_screen_btn]
        )


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

        body = ft.Column(
            [header.build(), project_list],
            spacing=0
        )

        create_project_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=ColorPalette.MAIN,
            foreground_color='#fff',
            margin=ft.Margin(0, 0, 30, 30),
            right=0,
            bottom=0,
            on_click=lambda: self._page.navigate(RouterPaths.PROJECT_CREATION)
        )

        screen_content = ft.Stack([body, create_project_button])
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

    def _go_to_project_screen(self, project: Project):
        '''Переход на экран проекта.'''

        store.current_project = project
        self._page.navigate(RouterPaths.PROJECT)

    def update_project_list(self):
        '''Обновление листа проектов.'''

        self._project_list_content.controls.clear()
        self._project_list_content.controls = self._get_projects()
