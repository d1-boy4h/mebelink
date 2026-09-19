from datetime import timedelta

import flet as ft

from ...constants import ColorPalette, ProjectStatus, RouterPaths
from ...services import ProjectService
from ..components import ExportProjectButton, Header
from ..store import store
from ..utils import show_notify
from .base_screen import BaseScreen


class ProjectSettingsScreen(BaseScreen):
    '''Экран настроек проекта.'''

    def __init__(self, page: ft.Page, project_service: ProjectService):
        super().__init__(page)
        self._project_service = project_service

    def build(self, route: str) -> ft.View:
        '''Сборка интерфейса экрана.'''

        if store.current_project is None:
            raise RuntimeError('Такого проекта не существует')

        export_project_btn = ExportProjectButton(
            self._page, self._project_service
        )

        self._header_component = Header(
            store.current_project.title,
            on_back=self._save_project,
            extra_buttons=[export_project_btn.build()]
        )

        header = self._header_component.build()

        self._title = ft.TextField(
            hint_text='Нужно заполнить!',
            label='Название проекта',
            text_size=16,
            hint_style=ft.TextStyle(color=ColorPalette.RED),
            value=store.current_project.title,
            on_change=self._button_switch,
            expand=True
        )

        address_text = ''
        if store.current_project.address:
            address_text = store.current_project.address

        self._address = ft.TextField(
            hint_text='ул. Пушкина, д. Колотушкина',
            label='Адрес',
            hint_style=ft.TextStyle(color=ColorPalette.GRAY),
            value=address_text,
            expand=True
        )

        phone_number = ''
        if store.current_project.phone:
            phone_number = store.current_project.phone

        self._phone = ft.TextField(
            hint_text='+79123456789',
            label='Номер телефона',
            hint_style=ft.TextStyle(color=ColorPalette.GRAY),
            keyboard_type=ft.KeyboardType.PHONE,
            input_filter=ft.InputFilter(r'^[0-9+]*$'),
            max_length=12,
            value=phone_number,
            expand=True
        )

        self._status = ft.Dropdown(
            store.current_project.status,
            label='Статус',
            options=[
                ft.DropdownOption(
                    key=status,
                    text=status.ru,
                    content=ft.Row([
                        ft.Icon(ft.Icons.CIRCLE, color=status.color, size=20),
                        ft.Text(status.ru)
                    ]),
                )
            for status in ProjectStatus],
            expand=True
        )

        self._improvements = ft.Checkbox(
            value=store.current_project.is_improvements,
            label='Есть доделки?',
            label_style=ft.TextStyle(size=16),
            active_color=ColorPalette.RED,
            margin=ft.Margin.all(0)
        )

        self._start_date = store.current_project.start_date.replace()

        self._start_date_picker = ft.DatePicker(
            value=self._start_date,
            locale=ft.Locale('ru'),
            help_text='Дата начала проекта',
            on_change=self._handle_change_start_date
        )

        self._end_date = None
        if store.current_project.end_date:
            self._end_date = store.current_project.end_date.replace()

        self._end_date_picker = ft.DatePicker(
            value=self._end_date,
            locale=ft.Locale('ru'),
            help_text='Дата конца проекта',
            on_change=self._handle_change_end_date
        )

        self._start_date_button = ft.Button(
            self._start_date.strftime('%d.%m.%y'),
            expand=True,
            on_click=lambda _: self._page.show_dialog(self._start_date_picker)
        )

        self._end_date_button = ft.Button(
            self._end_date.strftime('%d.%m.%y') if self._end_date else '-',
            expand=True,
            on_click=lambda _: self._page.show_dialog(self._end_date_picker)
        )

        dates_buttons = ft.Row(
            [self._start_date_button, ft.Text('/'), self._end_date_button],
            expand=True
        )

        title = self._get_wrapper(self._title, ft.Icons.TITLE)
        address = self._get_wrapper(self._address, ft.Icons.LOCATION_ON)
        phone = self._get_wrapper(self._phone, ft.Icons.PHONE)
        status = self._get_wrapper(self._status, ft.Icons.CONSTRUCTION)
        improvements = self._get_wrapper(self._improvements, ft.Icons.BUILD)
        dates = self._get_wrapper(dates_buttons, ft.Icons.DATE_RANGE)

        self._save_button = ft.Button(
            'Сохранить изменения',
            color='#fff',
            bgcolor=ColorPalette.GREEN,
            on_click=self._save_project,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.all(15)
            )
        )

        settings_list = ft.ListView(
            controls=[
                title,
                address,
                phone,
                status,
                improvements,
                dates,
                self._save_button
            ],
            spacing=15,
            padding=ft.Padding.all(20)
        )

        body = ft.Container(
            settings_list,
            bgcolor=ColorPalette.BACKGROUND,
            expand=True,
            width=float('inf')
        )

        screen_content = ft.Column([header, body], spacing=0)
        appbar_wrapper = ft.SafeArea(screen_content, expand=True)
        return ft.View([appbar_wrapper], route, padding=0)

    def _get_wrapper(
        self, content: ft.Control, icon: ft.IconData
    ) -> ft.Control:
        '''Возвращает белый блок с контентом.'''

        icon_color = ColorPalette.MAIN
        return ft.Container(
            ft.Row([ft.Icon(icon, icon_color, 20), content], spacing=10),
            bgcolor='#fff',
            border_radius=10,
            padding=ft.Padding(10, 15, 20, 10)
        )

    def _save_project(self, _):
        '''Сохранение проекта.'''

        if store.current_project is None:
            return

        old_project = store.current_project.model_copy()
        project = store.current_project
        project.title = self._title.value
        project.address = self._address.value if self._address.value else None
        project.phone = self._phone.value if self._phone.value else None

        if self._status.value:
            project.status = ProjectStatus(self._status.value)

        if self._improvements.value is not None:
            project.is_improvements = self._improvements.value

        project.start_date = self._start_date
        project.end_date = self._end_date

        if old_project != project:
            self._project_service.update_project(project)
            show_notify(self._page, 'Проект успешно сохранён')

        self._page.navigate(RouterPaths.PROJECT)

    def _button_switch(self, _):
        '''Выключает кнопку сохранения, если в title проекта пуст.'''

        self._save_button.disabled = not self._title.value

        if not self._title.value:
            self._save_button.bgcolor = ColorPalette.GRAY
            self._title.border_color = ColorPalette.RED
        else:
            self._save_button.bgcolor = ColorPalette.GREEN
            self._title.border_color = '#000'

    def _handle_change_start_date(self, e: ft.Event[ft.DatePicker]):
        '''Обработка выбора даты старта проекта.'''

        if e.control.value:
            raw_date = e.control.value.date() # type: ignore
            new_date = raw_date + timedelta(days=1)

            if self._end_date and new_date > self._end_date:
                show_notify(
                    self._page,
                    'Дата начала проекта должна быть раньше его завершения',
                    True
                )
                self._start_date_picker.value = self._start_date

            self._start_date = new_date
            self._start_date_button.content = new_date.strftime('%d.%m.%y')
            self._start_date_picker.value = new_date

    def _handle_change_end_date(self, e: ft.Event[ft.DatePicker]):
        '''Обработка выбора даты завершения проекта.'''

        if e.control.value:
            raw_date = e.control.value.date() # type: ignore
            new_date = raw_date + timedelta(days=1)

            if new_date < self._start_date:
                show_notify(
                    self._page,
                    'Дата завершения проекта должна быть позже его начала!',
                    is_error=True
                )
                self._end_date_picker.value = self._end_date

            self._end_date = new_date
            self._end_date_button.content = new_date.strftime('%d.%m.%y')
            self._end_date_picker.value = new_date
        else:
            self._end_date_button.content = '-'
