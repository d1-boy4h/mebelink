import asyncio

import flet as ft

from ...constants import ColorPalette, ImportConflictAction, RouterPaths
from ...models import Project
from ...services import ProjectService
from ..components import Header
from ..store import store
from ..utils import show_notify
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
            multiline=True,
            autofocus=True
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

        create_project_btn = ft.Button(
            'Создать проект',
            color='#fff',
            bgcolor=ColorPalette.GREEN,
            expand=True,
            style=btn_style,
            on_click=lambda: self._create_project(self._title_input.value)
        )

        self._import_project_btn = ft.Button(
            'Импортировать проект из файла',
            color='#fff',
            bgcolor=ColorPalette.MAIN,
            expand=True,
            style=btn_style,
            on_click=self._on_import_project_btn_click
        )

        elements_list = ft.ListView(
            controls=[
                title,
                create_project_btn,
                self._import_project_btn
            ],
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

    def _create_project(self, data: str | Project):
        '''Создание проекта.'''

        new_project = self._project_service.create_project(data)
        self._go_to_project_screen(new_project)

    async def _on_import_project_btn_click(self, _):
        '''Обработчик нажатия на кнопку импорта проекта.'''

        self._import_project_btn.disabled = True
        self._import_project_btn.bgcolor = ColorPalette.GRAY

        try:
            file_picker = ft.FilePicker()

            project = await file_picker.pick_files(
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=['mblp']
            )

            if len(project) and project[0].path is not None:
                try:
                    new_project = await self._project_service.import_from_mblp(
                        project[0].path,
                        self._show_import_conflict_modal
                    )

                    if new_project is not None:
                        self._go_to_project_screen(new_project)
                        show_notify(
                            self._page,
                            f'Проект "{new_project.title}" успешно импортирован'
                        )

                except TypeError as error:
                    show_notify(self._page, str(error), is_error=True)

        except RuntimeError as error:
            show_notify(self._page, str(error), is_error=True)

        finally:
            self._import_project_btn.disabled = False
            self._import_project_btn.bgcolor = ColorPalette.MAIN

        self._page.update()

    async def _show_import_conflict_modal(self) -> ImportConflictAction:
        '''Отображение модального окна в случае конфликта импорта проектов.'''

        loop = asyncio.get_running_loop()
        future: asyncio.Future[ImportConflictAction] = loop.create_future()

        def resolve(action: ImportConflictAction):
            if not future.done():
                future.set_result(action)

        btn_style = ft.ButtonStyle(
            text_style=ft.TextStyle(size=18),
            padding=ft.Padding.all(20)
        )

        duplicate_btn = ft.Button(
            content='Дублировать',
            color='#fff',
            bgcolor=ColorPalette.MAIN,
            style=btn_style,
            width=float('inf'),
            on_click=lambda _: (
                resolve(ImportConflictAction.DUPLICATE),
                self._page.pop_dialog()
            )
        )

        overwrite_btn = ft.Button(
            content='Перезаписать',
            color='#fff',
            bgcolor=ColorPalette.RED,
            style=btn_style,
            width=float('inf'),
            on_click=lambda _: (
                resolve(ImportConflictAction.OVERWRITE),
                self._page.pop_dialog()
            )
        )

        modal = ft.AlertDialog(
            title='Выбранный проект уже существует в каталоге',
            title_text_style=ft.TextStyle(size=18, color='#000'),
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[duplicate_btn, overwrite_btn],
            actions_overflow_button_spacing=10,
            bgcolor='#fff',
            on_dismiss=lambda _: resolve(ImportConflictAction.CANCEL)
        )

        self._page.show_dialog(modal)

        return await future
