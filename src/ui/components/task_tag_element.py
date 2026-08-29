import flet as ft

from ...constants import ColorPalette
from ...models import TaskTag


class TaskTagElement:
    '''Элемент выпадающего списка (раздела) с задачми проекта.'''

    def __init__(self, tag: TaskTag):
        self._tag = tag

    def build(self) -> ft.Control:
        '''Сборка интерфейса элемента.'''

        title = ft.Text(self._tag.title, expand=True)

        self._edit_btn = ft.IconButton(
            icon=ft.Icons.EDIT,
            icon_color=ColorPalette.MAIN,
            visible=False
        )

        self._delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ColorPalette.RED,
            visible=False
        )

        btn_wrapper = ft.Row([self._edit_btn, self._delete_btn], spacing=0)
        tile_title_wrapper = ft.Row([title, btn_wrapper], spacing=0)

        return ft.ExpansionTile(
            title=tile_title_wrapper,
            controls=[ft.Text('456')],
            bgcolor='#fff',
            collapsed_bgcolor='#fff',
            shape=ft.RoundedRectangleBorder(radius=10),
            collapsed_shape=ft.RoundedRectangleBorder(radius=10),
            controls_padding=ft.Padding(20, 15, 20, 10),
            on_change=self._switch_buttons_visible_handler
        )

    def _switch_buttons_visible_handler(self, e: ft.Event[ft.ExpansionTile]):
        '''Перключение видимости кнопок раздела при клике на него.'''

        self._edit_btn.visible = bool(e.data)
        self._delete_btn.visible = bool(e.data)
