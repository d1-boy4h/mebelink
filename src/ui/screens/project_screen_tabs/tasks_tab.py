import flet as ft

from ....services import TaskService, TaskTagService
from ...components import TagCreationButton, TaskTagElement
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

        self.refresh()
        return self._tags_listview

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

        self._tag_creation_btn = TagCreationButton(
            self._task_tag_service,
            self.refresh
        )
        tag_elements.append(self._tag_creation_btn.build())
        self._tags_listview.controls = tag_elements
        self._page.update()
