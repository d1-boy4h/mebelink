import flet as ft

from ....constants import ColorPalette, RouterPaths
from ....services import ProjectService
from ...components import Header
from ...store import store
from ..base_screen import BaseScreen
from .tabs import ActionsTab, EditingTab


class ProjectSettingsScreen(BaseScreen):
    '''Экран настроек проекта.'''

    def __init__(self, page: ft.Page, project_service: ProjectService):
        super().__init__(page)
        self._project_service = project_service

    def build(self, route: str) -> ft.View:
        '''Сборка интерфейса экрана.'''

        if store.current_project is None:
            raise RuntimeError('Такого проекта не существует')

        editing_tab = EditingTab(self._page, self._project_service)
        actions_tab = ActionsTab(self._page, self._project_service)

        to_settings_screen_btn = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_color='#fff',
            on_click=lambda: self._page.navigate(
                RouterPaths.SETTINGS
            )
        )

        self._header_component = Header(
            store.current_project.title,
            on_back=editing_tab.save_project,
            extra_buttons=[to_settings_screen_btn]
        )

        header = self._header_component.build()

        tab_bar = ft.TabBar(
            tabs=[
                ft.Tab(ft.Row([
                    ft.Icon(ft.Icons.EDIT_NOTE), ft.Text('Данные')
                ])),
                ft.Tab(ft.Row([
                    ft.Icon(ft.Icons.MORE_HORIZ), ft.Text('Действия')
                ]))
            ],
            indicator_color=ColorPalette.MAIN,
            label_color=ColorPalette.MAIN,
            unselected_label_color=ColorPalette.GRAY,
            tab_alignment=ft.TabAlignment.CENTER
        )

        tab_bar_view = ft.TabBarView(
            expand=True,
            controls=[
                ft.Container(editing_tab.build()),
                ft.Container(actions_tab.build())
            ],
        )

        tabs = ft.Tabs(
            ft.Column([tab_bar, tab_bar_view]),
            length=len(tab_bar.tabs),
            expand=True
        )

        body = ft.Container(
            tabs,
            bgcolor=ColorPalette.BACKGROUND,
            width=float('inf'),
            expand=True
        )

        screen_content = ft.Column([header, body], spacing=0)
        appbar_wrapper = ft.SafeArea(screen_content, expand=True)
        return ft.View([appbar_wrapper], route, padding=0)
