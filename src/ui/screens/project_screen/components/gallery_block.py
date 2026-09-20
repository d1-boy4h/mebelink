import asyncio
import logging

import flet as ft

from .....constants import ColorPalette
from .....services import FileService
from ....store import store
from ....utils import show_notify
from .image_viewer import ImageViewer


class GalleryBlock:
    '''Блок с галереей эскизов проекта.'''

    def __init__(self, page: ft.Page, file_service: FileService):
        self._page = page
        self._file_service = file_service

        self._viewer = ImageViewer(page, file_service, self.refresh)
        self._logger = logging.getLogger(self.__class__.__name__)

    def build(self) -> ft.Control:
        '''Построение интерфейса блока.'''

        self._file_picker = ft.FilePicker()
        self._file_picker_btn = ft.IconButton(
            ft.Icons.FILE_UPLOAD,
            bgcolor=ColorPalette.MAIN,
            icon_color='#fff',
            icon_size=28,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=self._open_file_picker
        )

        self._gallery = ft.GridView(runs_count=4)
        self.refresh()

        return ft.Container(
            self._gallery,
            bgcolor='#fff',
            border_radius=10,
            padding=ft.Padding(10, 15, 10, 10),
            alignment=ft.Alignment.TOP_LEFT
        )

    def refresh(self):
        '''Обновление фотографий при переключении проекта.'''

        if store.current_project is None:
            return

        files = self._file_service.get_all(store.current_project.uuid)
        store.current_files = files[:]

        gallery_elements = []
        for file in files:
            image = ft.Image(
                src=file.path,
                fit=ft.BoxFit.FILL,
                cache_width=300,
                cache_height=300
            )

            file_btn = ft.Container(
                image,
                border_radius=10,
                on_click=lambda _, f=file: self._viewer.open(f)
            )

            gallery_elements.append(file_btn)

        gallery_elements.append(self._file_picker_btn)
        self._gallery.controls = gallery_elements

    async def _open_file_picker(self, _):
        '''Обработка нажатия кнопки загрузки фотографий.'''

        if store.current_project is None:
            return

        try:
            self._file_picker_btn.disabled = True
            self._file_picker_btn.bgcolor = ColorPalette.GRAY

            files = await self._file_picker.pick_files(
                allow_multiple=True,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'bmp'],
                compression_quality=75
            )

            for file in files:
                if file.path is None:
                    continue

                try:
                    content = await asyncio.to_thread(
                        self._read_file_sync, file.path
                    )

                    self._file_service.save_file(
                        store.current_project.uuid,
                        file.name,
                        content
                    )

                except ValueError as e:
                    show_notify(self._page, f'{e}!', is_error=True)

        except Exception as e:  # noqa: BLE001
            show_notify(
                self._page,
                'Кажется, что-то сломалось... (подробности в логе)',
                is_error=True
            )

            self._logger.error(f'{e}')

        finally:
            self._file_picker_btn.disabled = False
            self._file_picker_btn.bgcolor = ColorPalette.MAIN

        self.refresh()
        self._page.update()

    def _read_file_sync(self, path: str) -> bytes:
        '''Синхронная функция чтения файла.'''
        with open(path, 'rb') as f:
            return f.read()
