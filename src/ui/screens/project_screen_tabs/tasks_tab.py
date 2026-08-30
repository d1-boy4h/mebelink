import flet as ft

from ....constants import ColorPalette
from ....services import TaskService, TaskTagService
from ...components import TaskTagElement
from ...store import store


class TasksTab:
    '''Вкладка с задачами проекта.'''

    def __init__(
            self,
            page: ft.Page,
            task_tag_service: TaskTagService,
            task_service: TaskService
        ):
        self._page = page
        self._task_tag_service = task_tag_service
        self._task_service = task_service

    def build(self) -> ft.Control:
        '''Сборка интерфейса вкладки.'''

        self._project = store.current_project
        if self._project is None:
            raise RuntimeError('Такого проекта не существует')

        self._tags_listview = ft.ListView(
            controls=[],
            spacing=20,
            padding=ft.Padding(20, 0, 20, 20)
        )

        create_tag_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=ColorPalette.MAIN,
            foreground_color='#fff',
            margin=ft.Margin(0, 0, 30, 30),
            right=0,
            bottom=0,
            on_click=self._show_create_task_tag_modal
        )

        self.refresh()

        return ft.Stack([self._tags_listview, create_tag_button])

    def refresh(self):
        '''Обновление списка разделов задач.'''

        if self._project is None:
            return

        tags = self._task_tag_service.get_all(self._project.uuid)
        store.current_tags = tags[:]

        tag_elements = []
        for tag in tags:
            task_tag_element = TaskTagElement(
                tag,
                self._page,
                self._task_tag_service,
                self._task_service,
                self.refresh
            )
            tag_elements.append(task_tag_element.build())

        self._tags_listview.controls = tag_elements
        self._page.update()

    def _show_create_task_tag_modal(self, _):
        '''Отображение модального окна создания раздела для задач.'''

        self._text_input = ft.TextField(
            hint_text='Новый раздел',
            autofocus=True,
            border=ft.InputBorder.NONE,
            text_size=20
        )

        accept_button = ft.Button(
            'создать',
            on_click=lambda _: self._create_tag(self._text_input.value),
            color='#fff',
            width=float('inf'),
            style=ft.ButtonStyle(
                bgcolor=ColorPalette.MAIN,
                text_style=ft.TextStyle(size=18),
                padding=ft.Padding(20, 15, 20, 15)
            )
        )

        modal = ft.AlertDialog(
            self._text_input,
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[accept_button],
            bgcolor='#fff'
        )

        self._page.show_dialog(modal)

    def _create_tag(self, title: str):
        '''Создание раздела задач в модальном окне.'''

        if self._project is None:
            return

        self._task_tag_service.create(title, self._project.uuid)

        self.refresh()
        self._page.pop_dialog()
        self._page.update()
