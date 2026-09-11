from asyncio import sleep
from collections.abc import Callable
from typing import ClassVar, Literal

import flet as ft

from ...constants import ColorPalette
from ...models import File
from ...services import FileService
from ..store import store

ImageSwipingDirType = Literal['left', 'right']

class Constants:
    '''Константы для обработки жестов.'''

    MIN_SCALE_MOVE: ClassVar[float] = 0.001
    MIN_SCALE: ClassVar[float] = 0.5
    BASE_SCALE: ClassVar[float] = 1.0
    MAX_SCALE: ClassVar[float] = 5.0

    OFFSET_IMAGE_CHANGE: ClassVar[float] = 0.35
    VELOCITY_THRESHOLD: ClassVar[float] = 700.0
    FPS: ClassVar[int] = 60
    ANIMATION_MS: ClassVar[int] = 150

    BASE_ANIMATION: ClassVar[ft.Animation] = ft.Animation(
        ANIMATION_MS, ft.AnimationCurve.EASE_OUT
    )

    SWIPE_ANIMATION_IN: ClassVar[ft.Animation] = ft.Animation(
        ANIMATION_MS, ft.AnimationCurve.EASE_IN
    )

    SWIPE_ANIMATION_OUT: ClassVar[ft.Animation] = ft.Animation(
        ANIMATION_MS, ft.AnimationCurve.EASE_OUT
    )

class ImageViewer:
    '''Компонент просмотра фотографий проекта.'''

    def __init__(
            self,
            page: ft.Page,
            file_service: FileService,
            refresh_callback: Callable):
        self._page = page
        self._file_service = file_service
        self._refresh_callback = refresh_callback

        self._width = page.width if page.width is not None else 1
        self._height = page.height if page.height is not None else 1

        self._files: list[File] | None = None
        self._file_index: int | None = None

        self._offset: tuple[float, float] | None = None
        self._initial_scale: float | None = None
        self._scale: float | None = None
        self._image: ft.Image | None = None
        self._container: ft.SafeArea | None = None

        self._image_swiping_dir: ImageSwipingDirType | None = None
        self._swipe_velocity: float = 0.0

    def open(self, file: File):
        '''Открытие полноэкранного просмотра.'''

        self._page.views[-1].can_pop = False

        self._files = store.current_files
        if self._files is None:
            return

        self._file_index = self._files.index(file)

        self._image = ft.Image(
            self._files[self._file_index].path,
            fit=ft.BoxFit.CONTAIN,
            width=self._page.width,
            height=self._page.height,
            opacity=1,
            animate_offset=Constants.BASE_ANIMATION,
            animate_scale=Constants.BASE_ANIMATION,
            animate_opacity=Constants.BASE_ANIMATION
        )

        self._image.offset = self._offset = (0, 0)
        self._image.scale = self._scale = Constants.BASE_SCALE

        gesture_detector = ft.GestureDetector(
            content=self._image,
            drag_interval=16,
            on_scale_start=self._on_scale_start,
            on_scale_update=self._on_scale_update,
            on_scale_end=self._on_scale_end
        )

        container_content = ft.Container(
            content=ft.Stack([
                ft.Container(
                    gesture_detector,
                    bgcolor=ft.Colors.with_opacity(0.9, '#000')
                ),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    icon_color='#fff',
                    icon_size=32,
                    on_click=lambda _: self._close(),
                    right=0,
                    margin=ft.Margin.all(10)
                ),
                ft.IconButton(
                    ft.Icons.DELETE,
                    icon_color=ColorPalette.RED,
                    icon_size=32,
                    on_click=self._show_delete_file_modal,
                    right=0,
                    bottom=0,
                    margin=ft.Margin.all(10)
                ),
            ], expand=True)
        )

        self._container = ft.SafeArea(container_content, expand=True)
        self._page.overlay.append(self._container)

    def _close(self):
        '''Закрытие полноэкранного просмотра.'''

        self._page.views[-1].can_pop = True

        if self._container and self._container in self._page.overlay:
            self._page.overlay.remove(self._container)

            self._container = None
            self._image = None
            self._offset = None
            self._scale = None

    def _on_scale_start(self, _):
        '''Сохранение скейла в начале жеста.'''

        if self._scale is None:
            return

        self._initial_scale = self._scale

    def _on_scale_update(self, e: ft.ScaleUpdateEvent):
        '''Обработка жестов.'''

        ft.context.disable_auto_update()

        if self._image is None or \
            self._offset is None or \
            self._scale is None or \
            self._file_index is None:
            return

        if e.scale != Constants.BASE_SCALE and \
            self._initial_scale is not None:
            new_scale = self._initial_scale * e.scale
            new_scale = max(
                Constants.MIN_SCALE,
                min(Constants.MAX_SCALE, new_scale)
            )

            if abs(new_scale - self._scale) > Constants.MIN_SCALE_MOVE:
                self._scale = new_scale
                self._image.scale = self._scale

        delta_x = e.focal_point_delta.x / self._width
        delta_y = e.focal_point_delta.y / self._height

        offset_x = self._offset[0] + delta_x
        offset_y = 0.0

        if self._scale == Constants.BASE_SCALE:
            swipe_velocity = delta_x * self._width * Constants.FPS

            if abs(offset_x) > Constants.OFFSET_IMAGE_CHANGE:
                self._image_swiping_dir = 'left' if offset_x < 0 else 'right'
                self._image.opacity = 0.6

            elif abs(swipe_velocity) >= Constants.VELOCITY_THRESHOLD:
                self._image_swiping_dir = 'left' if swipe_velocity < 0 \
                    else 'right'

            else:
                self._image_swiping_dir = None
                self._image.opacity = 1

        else:
            offset_y = self._offset[1] + delta_y

        self._image.offset = self._offset = (offset_x, offset_y)
        self._image.update()

    def _on_scale_end(self, _):
        '''Перехватчик жестов после их завершения.'''

        if self._image is None or \
            self._offset is None or \
            self._scale is None:
            return

        self._initial_scale = None

        if self._image_swiping_dir is not None:
            self._page.run_task(self._on_change_image)
            return

        if self._scale <= Constants.BASE_SCALE:
            self._image.animate_offset = Constants.BASE_ANIMATION
            self._image.animate_scale = Constants.BASE_ANIMATION
            self._image.scale = self._scale = Constants.BASE_SCALE
            self._image.offset = self._offset = (0, 0)

        self._image_swiping_dir = None
        self._image.opacity = 1

    async def _on_change_image(self):
        '''Обработка смены изображения.'''

        ft.context.disable_auto_update()

        if self._image is None or \
            self._offset is None or \
            self._files is None or \
            self._file_index is None:
            return

        self._image.animate_offset = Constants.SWIPE_ANIMATION_IN
        self._image.opacity = 1
        push_out_x = -1.0 if self._image_swiping_dir == 'left' else 1.0
        self._image.offset = (push_out_x, 0)
        self._image.update()

        await sleep(Constants.ANIMATION_MS / 1000.0)

        files_count = len(self._files)

        if self._image_swiping_dir == 'left':
            if self._file_index + 1 == files_count:
                self._file_index = 0
            else:
                self._file_index += 1
        elif self._image_swiping_dir == 'right':
            if self._file_index - 1 < 0:
                self._file_index = files_count - 1
            else:
                self._file_index -= 1

        self._image.src = self._files[self._file_index].path
        self._image.animate_offset = ft.Animation()
        start_x = 1.0 if self._image_swiping_dir == 'left' else -1.0
        self._image.offset = (start_x, 0)
        self._image.scale = self._scale = Constants.BASE_SCALE
        self._image.update()

        await sleep(0.05)

        self._image.animate_offset = Constants.SWIPE_ANIMATION_OUT
        self._image.offset = self._offset = (0, 0)
        self._image.update()

        await sleep(Constants.ANIMATION_MS / 1000.0)

        self._image.animate_offset = Constants.BASE_ANIMATION
        self._image_swiping_dir = None
        self._image.update()

    def _show_delete_file_modal(self, _):
        '''Отображение модального окна подтверждения удаления изображения.'''

        accept_button = ft.Button(
            'Да, удалить',
            on_click=self._on_file_delete,
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

    def _on_file_delete(self, _):
        '''Удаление проекта.'''

        if self._files is None or self._file_index is None:
            return

        file = self._files[self._file_index]
        if file.id is not None:
            self._file_service.delete_file(file)
            self._refresh_callback()
            self._page.pop_dialog()
            self._close()

            self._page.update()
