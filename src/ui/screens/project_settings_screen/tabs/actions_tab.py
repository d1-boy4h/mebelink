from pathlib import Path

import flet as ft

from .....constants import RouterPaths
from .....services import ProjectService
from ....components import ColorPalette
from ....store import store
from ....utils import show_notify


class ActionsTab:
    '''Вкладка с действиями над проектом.'''

    def __init__(self, page: ft.Page, project_service: ProjectService):
        self._page = page
        self._project_service = project_service

    def build(self) -> ft.Control:
        '''Сборка интерфейса вкладки.'''

        btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.all(20)
        )

        self._export_project_btn = ft.Button(
            content='Экспортировать проект в файл',
            color='#fff',
            bgcolor=ColorPalette.MAIN,
            on_click=self._export_project,
            style=btn_style
        )

        delete_btn = ft.Button(
            content='Удалить проект',
            color='#fff',
            bgcolor=ColorPalette.RED,
            on_click=self._show_delete_project_modal,
            style=btn_style
        )

        return ft.ListView(
            controls=[self._export_project_btn, delete_btn],
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

        if project is None:
            return

        self._project_service.delete_project(project.uuid)

        store.current_project = None
        store.current_files = None

        self._page.navigate(RouterPaths.HOME)
        self._page.pop_dialog()

    async def _export_project(self, _):
        '''Обработка нажатия кнопки экспорта проекта.'''

        if store.current_project is None:
            return

        self._export_project_btn.disabled = True
        self._export_project_btn.icon_color = ColorPalette.GRAY

        try:
            mblp_bytes = self._project_service.export_to_mblp(
                store.current_project.uuid
            )

            file_picker = ft.FilePicker()
            path = await file_picker.save_file(
                dialog_title='Сохранение проекта в файл...',
                file_name=f'{store.current_project.title}.mblp',
                src_bytes=mblp_bytes
            )

            if path is not None:
                if self._page.platform != ft.PagePlatform.ANDROID:
                    Path(path).write_bytes(mblp_bytes)

                    show_notify(
                        page=self._page,
                        text=f'Проект успешно экспортирован:\n{path}'
                    )

                else:
                    show_notify(self._page, 'Проект успешно экспортирован')

        except RuntimeError as error:
            show_notify(
                self._page,
                str(error),
                is_error=True
            )

        finally:
            self._export_project_btn.disabled = False
            self._export_project_btn.icon_color = '#fff'

        self._page.update()
