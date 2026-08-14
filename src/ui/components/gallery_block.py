import flet as ft

from ...constants import ColorPalette
from ...services import FileService
from ..store import store
from .image_viewer import ImageViewer


class GalleryBlock:
    '''Блок с галереей эскизов проекта.'''

    def __init__(self, page: ft.Page, file_service: FileService):
        self._page = page

        self._file_service = file_service
        self._viewer = ImageViewer(page)

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
            image = ft.Image(file.path, fit=ft.BoxFit.FILL)
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

        files = await self._file_picker.pick_files(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.IMAGE,
            with_data=True
        )

        for file in files:
            if file.bytes is None:
                continue

            try:
                self._file_service.save_file(
                    store.current_project.uuid,
                    file.name,
                    file.bytes
                )

            except ValueError as e:
                self._show_error_notif(f'{e}!')

        self.refresh()

    def _show_error_notif(self, text: str):
        '''Получение всплывашки ошибки с текстом для повторного файла.'''

        notif = ft.SnackBar(
            content=text,
            behavior=ft.SnackBarBehavior.FLOATING,
            bgcolor=ColorPalette.RED
        )

        self._page.show_dialog(notif)
