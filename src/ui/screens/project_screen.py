import flet as ft

from ...constants import ColorPalette, RouterPaths
from ...services import FileService, ProjectService
from ..components import Header
from ..store import store
from .base_screen import BaseScreen
from .project_screen_tabs import MainTab


class ProjectScreen(BaseScreen):
    '''Экран проекта.'''

    def __init__(
        self,
        page: ft.Page,
        project_service: ProjectService,
        file_service: FileService
    ):
        super().__init__(page)

        self._project_service = project_service
        self._file_service = file_service

    def build(self, route: str) -> ft.View:
        '''Сборка интерфейса экрана.'''

        self._project = store.current_project
        if self._project is None:
            raise RuntimeError('Такого проекта не существует')

        self._header_component = Header(
            self._project.title,
            on_back=self._back_to_home_screen_handler
        )

        header = self._header_component.build()

        tab_bar = ft.TabBar(
            tabs=[
                ft.Tab(ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT), ft.Text('Главная')
                ])),
                ft.Tab(ft.Row([
                    ft.Icon(ft.Icons.CHECKLIST), ft.Text('Задачи')
                ])),
                ft.Tab(ft.Row([
                    ft.Icon(ft.Icons.SETTINGS), ft.Text('Настройки')
                ]))
            ],
            indicator_color=ColorPalette.MAIN,
            label_color=ColorPalette.MAIN,
            unselected_label_color=ColorPalette.GRAY,
        )

        self._main_tab = MainTab(
            self._page,
            self._header_component,
            self._project_service,
            self._file_service
        )

        tab_bar_view = ft.TabBarView(
            expand=True,
            margin=ft.Margin.all(20),
            controls=[
                ft.Container(self._main_tab.build()),
                ft.Container(
                    content=ft.Text('Tasks content'),
                ),
                ft.Container(
                    content=ft.Text('Settings content'),
                ),
            ],
        )

        tabs = ft.Tabs(
            ft.Column(controls=[tab_bar, tab_bar_view]),
            length=3,
            expand=True
        )

        # body_content = ft.PageView(
        #     [self._project_info_screen.build(), ft.Text('123')],
        #     implicit_scrolling=True
        # )

        body = ft.Container(
            tabs,
            bgcolor=ColorPalette.BACKGROUND,
            width=float('inf'),
            expand=True
        )

        screen_content = ft.Column([header, body], spacing=0)
        appbar_wrapper = ft.SafeArea(screen_content, expand=True)
        return ft.View([appbar_wrapper], route, padding=0)

    def _on_project_delete(self, _):
        '''Удаление проекта.'''

        project = store.current_project
        if project is None: return

        self._project_service.delete_project(project.uuid)
        store.current_project = None
        store.current_files = None
        self._page.navigate(RouterPaths.HOME_SCREEN)
        self._page.pop_dialog()

    def update_project_info(self):
        '''Обновление информации о проекте.'''

        if self._project is None:
            return

        self._header_component.title = self._project.title
        self._main_tab.update_blocks()

    def _back_to_home_screen_handler(self, _):
        '''Коллбэк перехода на домашний экран для шапки.'''

        store.current_project = None
        store.current_files = None
        self._page.navigate(RouterPaths.HOME_SCREEN)
