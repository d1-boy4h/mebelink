from abc import ABC, abstractmethod

import flet as ft


class BaseScreen(ABC):
    '''Базовый класс для экранов.'''

    def __init__(self, page: ft.Page):
        self._page = page

    @abstractmethod
    def build(self, route: str) -> ft.View:
        '''Постройка интерфейса экрана.'''
