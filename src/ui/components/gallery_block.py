import flet as ft


class GalleryBlock:
    '''Блок с галереей эскизов проекта.'''

    def __init__(self):
        pass

    def build(self) -> ft.Control:
        '''Построение интерфейса блока.'''

        self._column = ft.Column()
        self.refresh()

        return ft.Container(
            self._column,
            bgcolor='#fff',
            border_radius=10,
            padding=ft.Padding(10, 15, 10, 10),
            alignment=ft.Alignment.TOP_LEFT
        )

    def refresh(self):
        '''Обновление фотографий при переключении проекта.'''

        return
