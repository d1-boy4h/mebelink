import flet as ft

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

        return ft.ListView(
            controls=[
                self._info_block.build(),
                self._gallery_block.build()
            ],
            spacing=15,
            padding=ft.Padding(20, 0, 20, 20)
        )

    def update_blocks(self):
        '''Обновление информации о проекте.'''

        self._info_block.refresh_rows()
        self._gallery_block.refresh()
