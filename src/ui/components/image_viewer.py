from typing import Literal

import flet as ft

from ...constants import ColorPalette
from ...models import File
from ..store import store

ImageSwipingDirType = Literal['left', 'right']

class ImageViewer:
    '''Компонент просмотра фотографий проекта.'''

    def __init__(self, page: ft.Page):
        self._page = page

        self._width = page.width if page.width is not None else 1
        self._height = page.height if page.height is not None else 1

        self._files: list[File] | None = None
        self._file_index: int | None = None

        self._offset: tuple[float, float] | None = None
        self._scale: float | None = None
        self._image: ft.Image | None = None
        self._container: ft.Container | None = None

        self._image_swiping_dir: ImageSwipingDirType | None = None

    def open(self, file: File):
        '''Открытие полноэкранного просмотра.'''

        self._close()

        self._offset = 0, 0
        self._scale = 1.0

        self._files = store.current_files
        if self._files is None:
            return

        self._file_index = self._files.index(file)

        self._image = ft.Image(
            self._files[self._file_index].path,
            fit=ft.BoxFit.CONTAIN,
            width=self._page.width,
            height=self._page.height,
            opacity=1
        )

        gesture_detector = ft.GestureDetector(
            content=self._image,
            on_scale_update=self._on_scale_update,
            on_scale_end=self._on_scale_end
        )

        self._container = ft.Container(
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
                    on_click=lambda _: self._close(),
                    right=0,
                    bottom=0,
                    margin=ft.Margin.all(10)
                ),
            ], expand=True)
        )

        self._page.overlay.append(self._container)

    def _close(self):
        '''Закрытие полноэкранного просмотра.'''

        if self._container and self._container in self._page.overlay:
            self._page.overlay.remove(self._container)

            self._container = None
            self._image = None
            self._offset = None
            self._scale = None

    def _on_scale_update(self, e: ft.ScaleUpdateEvent):
        '''Обработка жестов.'''

        if self._image is None or \
        self._offset is None or \
        self._scale is None or \
        self._file_index is None:
            return

        SCROLL_SPEED_LIMITER = 10

        if e.scale != 1.0:
            if e.scale > 1.0 and self._scale < 5:
                self._scale += (e.scale - 1.0) / SCROLL_SPEED_LIMITER
            elif e.scale < 1.0 and self._scale > 0.1:
                self._scale -= (1.0 - e.scale) / SCROLL_SPEED_LIMITER

            self._image.scale = self._scale

        offset_x = self._offset[0] + e.focal_point_delta.x / self._width
        offset_y = 0.0

        OFFSET_IMAGE_CHANGE_LIMIT = 0.4

        if self._scale > 1.0:
            offset_y = self._offset[1] + e.focal_point_delta.y / self._height
        else:
            if self._offset[0] < -OFFSET_IMAGE_CHANGE_LIMIT: # Свайп влево
                self._image_swiping_dir = 'left'
                self._image.opacity = 0.7
            elif self._offset[0] > OFFSET_IMAGE_CHANGE_LIMIT:  # Свайп вправо
                self._image_swiping_dir = 'right'
                self._image.opacity = 0.7
            else:
                self._image_swiping_dir = None
                self._image.opacity = 1

        self._offset = (offset_x, offset_y)
        self._image.offset = self._offset

    def _on_scale_end(self, _):
        '''Перехватчик жестов после их завершения.'''

        if self._image is None or \
        self._offset is None or \
        self._scale is None:
            return

        if self._scale <= 1.0 and self._image_swiping_dir is None:
            self._image.scale = self._scale = 1.0
            self._image.offset = self._offset = (0, 0)

        if self._image_swiping_dir is not None:
            self._on_change_image()

        self._image.opacity = 1

    def _on_change_image(self):
        '''Обработка смены изображения.'''

        if self._image is None or \
        self._offset is None or \
        self._files is None or \
        self._file_index is None:
            return

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
        self._image.offset = self._offset = (0, 0)
