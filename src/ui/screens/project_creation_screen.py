import flet as ft

from ...constants import ColorPalette, RouterPaths
from ...models import Project
from ...services import ProjectService
from ..components import Header
from ..store import store
from .base_screen import BaseScreen


class ProjectCreationScreen(BaseScreen):
    '''Экран создания проекта.'''

    def __init__(self, page: ft.Page, project_service: ProjectService):
        super().__init__(page)
        self._project_service = project_service

    def build(self, route: str) -> ft.View:
        '''Сборка интерфейса экрана.'''

        header = Header(
            'Создание проекта',
            on_back=lambda: self._page.navigate(RouterPaths.HOME)
        )

        self._title_input = ft.TextField(
            hint_text='Новый проект',
            label='Название проекта',
            text_size=16,
            border=ft.InputBorder.NONE,
            multiline=True
        )

        title = ft.Container(
            content=self._title_input,
            bgcolor='#fff',
            border_radius=10,
            padding=ft.Padding(10, 5, 20, 5)
        )

        btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.all(20)
        )

        create_btn = ft.Button(
            'Создать проект',
            color='#fff',
            bgcolor=ColorPalette.GREEN,
            expand=True,
            style=btn_style,
            on_click=self._create_project
        )

        import_btn = ft.Button(
            'Импортировать проект из файла',
            color='#fff',
            bgcolor=ColorPalette.MAIN,
            expand=True,
            style=btn_style,
            # on_click=
        )

        elements_list = ft.ListView(
            controls=[title, create_btn, import_btn],
            spacing=15,
            padding=ft.Padding.all(20)
        )

        body = ft.Container(
            content=elements_list,
            bgcolor=ColorPalette.BACKGROUND,
            expand=True,
            width=float('inf')
        )

        screen_content = ft.Column([header.build(), body], spacing=0)
        appbar_wrapper = ft.SafeArea(screen_content, expand=True)
        return ft.View([appbar_wrapper], route, padding=0)

    def _go_to_project_screen(self, project: Project):
        '''Переход в экран проекта.'''

        self._title_input.value = ''
        store.current_project = project
        self._page.navigate(RouterPaths.PROJECT)

    def _create_project(self, _):
        '''Создание проекта.'''

        title = self._title_input.value
        new_project = self._project_service.create_project(title)

        self._go_to_project_screen(new_project)
