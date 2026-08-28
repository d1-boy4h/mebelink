import flet as ft
from flet import run as run_flet_engine

from ..constants import ColorPalette, RouterPaths
from ..services import FileService, ProjectService, TaskService, TaskTagService
from .screens import BaseScreen, HomeScreen, ProjectScreen, ProjectSettingsScreen


class Interface:
    '''Корневой класс интерфейса.'''

    def __init__(
        self,
        project_service: ProjectService,
        file_service: FileService,
        task_tag_service: TaskTagService,
        task_service: TaskService
    ):
        self._project_service = project_service
        self._file_service = file_service
        self._task_tag_service = task_tag_service
        self._task_service = task_service

    def _get_screen(self, route: str) -> ft.View:
        '''Получение компонента страницы для навигации из пути.'''

        screen = self._screens.get(route)
        if screen is None:
            screen = self._screens[RouterPaths.HOME_SCREEN]

        return screen.build(route)

    def _on_route_change(self, e: ft.RouteChangeEvent):
        '''Обработка навигации по страницам (page.navigate).'''

        if e.route == self._current_route:
            return

        self._current_route: str = e.route

        view_list = self._page.views
        for index, view in enumerate(view_list):
            if e.route == view.route:
                new_view_list = view_list[:index+1]
                view_list.clear()
                view_list.extend(new_view_list)

                if e.route == RouterPaths.HOME_SCREEN:
                    home_screen = self._screens[RouterPaths.HOME_SCREEN]
                    home_screen.update_project_list() # type: ignore

                if e.route == RouterPaths.PROJECT_SCREEN:
                    project_screen = self._screens[RouterPaths.PROJECT_SCREEN]
                    project_screen.update_project_info() # type: ignore

                break

        else:
            view = self._get_screen(e.route)
            self._page.views.append(view)

        self._page.update()

    def _on_view_pop(self, _):
        '''Обработка кнопки "Назад" на смартфоне.'''

        view_list = self._page.views
        last_view = view_list[-2]
        self._page.navigate(last_view.route)

    def _setup(self, page: ft.Page):
        '''Инициализация Flet-приложения.'''

        self._page = page
        self._current_route = RouterPaths.HOME_SCREEN

        self._screens: dict[str, BaseScreen] = {
            RouterPaths.HOME_SCREEN: HomeScreen(page, self._project_service),
            RouterPaths.PROJECT_SCREEN: ProjectScreen(
                page, self._project_service, self._file_service
            ),
            RouterPaths.PROJECT_SETTINGS_SCREEN: ProjectSettingsScreen(
                page, self._project_service
            )
        }

        page.title = 'МебеЛинк'
        page.window.width = 360
        page.window.height = 660
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(
            system_overlay_style=ft.SystemOverlayStyle(
                status_bar_color=ColorPalette.MAIN,
            ),
            page_transitions=ft.PageTransitionsTheme(
                android=ft.PageTransitionTheme.CUPERTINO,
                ios=ft.PageTransitionTheme.CUPERTINO,
                windows=ft.PageTransitionTheme.CUPERTINO,
                macos=ft.PageTransitionTheme.CUPERTINO,
                linux=ft.PageTransitionTheme.CUPERTINO
            )
        )

        page.views.clear()
        page.on_route_change = self._on_route_change
        page.on_view_pop = self._on_view_pop

        page.views.append(self._get_screen(self._current_route))

    def run(self):
        '''Обёртка для функции run из Flet для инкапсуляции.'''
        run_flet_engine(self._setup)
