import flet as ft

from .....constants import ColorPalette, RouterPaths
from .....services import FileService, ProjectService
from ....store import store
from ..components import GalleryBlock, InfoBlock


class MainTab:
    '''Вкладка с информацией о проекте.'''

    def __init__(
        self,
        page: ft.Page,
        project_service: ProjectService,
        file_service: FileService
    ):
        self._page = page

        self._project_service = project_service
        self._file_service = file_service

    def build(self) -> ft.Control:
        '''Сборка интерфейса вкладки.'''

        self._project = store.current_project
        if self._project is None:
            raise RuntimeError('Такого проекта не существует')

        self._info_block = InfoBlock(self._project, self._page)
        self._gallery_block = GalleryBlock(self._page, self._file_service)

        delete_button = ft.Button(
            'Удалить проект',
            color='#fff',
            bgcolor=ColorPalette.RED,
            on_click=self._show_delete_project_modal,
            margin=ft.Margin.only(top=10),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.all(15)
            )
        )

        return ft.ListView(
            controls=[
                self._info_block.build(),
                self._gallery_block.build(),
                delete_button
            ],
            spacing=15,
            padding=ft.Padding(20, 0, 20, 20)
        )

    def _show_delete_project_modal(self, _):
        '''Отображение модального окна подтверждения удаления проекта.'''

        accept_button = ft.Button(
            'Да, удалить',
            on_click=self._on_project_delete,
            color='#fff',
            bgcolor=ColorPalette.RED,
            width=float('inf'),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=16),
                padding=ft.Padding(20, 15, 20, 15)
            )
        )

        modal = ft.AlertDialog(
            title='Вы уверены?',
            title_text_style=ft.TextStyle(size=20, color='#000'),
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[accept_button],
            bgcolor='#fff'
        )

        self._page.show_dialog(modal)

    def _on_project_delete(self, _):
        '''Удаление проекта.'''

        project = store.current_project
        if project is None: return

        self._project_service.delete_project(project.uuid)
        store.current_project = None
        store.current_files = None
        self._page.navigate(RouterPaths.HOME)
        self._page.pop_dialog()

    def update_blocks(self):
        '''Обновление информации о проекте.'''

        self._info_block.refresh_rows()
        self._gallery_block.refresh()
