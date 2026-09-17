import flet as ft

from ...constants import ColorPalette
from ...services import ProjectService
from ..store import store
from ..utils import show_notify


class ExportProjectButton:
    '''Кнопка экспорта проекта в файл.'''

    def __init__(self, page: ft.Page, project_service: ProjectService):
        self._page = page
        self._project_service = project_service

    def build(self) -> ft.Control:
        '''Сборка интерфейса.'''

        self._file_picker = ft.FilePicker()

        self._file_picker_btn = ft.IconButton(
            icon=ft.Icons.FOLDER_ZIP,
            icon_color='#fff',
            on_click=self._open_file_picker
        )

        return self._file_picker_btn

    async def _open_file_picker(self, _):
        '''Обработка нажатия кнопки загрузки фотографий.'''

        if store.current_project is None:
            return

        self._file_picker_btn.disabled = True
        self._file_picker_btn.icon_color = ColorPalette.GRAY

        try:
            path = await self._file_picker.save_file(
                dialog_title='Сохранение проекта в файл...',
                file_name=f'{store.current_project.title}.mblp'
            )

            if path is not None:
                # self._project_service.export_to_mblp(
                #     store.current_project.uuid, path
                # )

                show_notify(self._page, 'Проект успешно экспортирован')

        except _:
            show_notify(
                self._page,
                'Кажется, что-то сломалось...',
                is_error=True
            )

        finally:
            self._file_picker_btn.disabled = False
            self._file_picker_btn.icon_color = '#fff'

        self._page.update()
