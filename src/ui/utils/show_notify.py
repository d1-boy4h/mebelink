import flet as ft

from ...constants import ColorPalette


def show_notify(page: ft.Page, text: str, is_error: bool = False):
    '''Вызов всплывающего уведомления.'''

    notif = ft.SnackBar(
        content=text,
        behavior=ft.SnackBarBehavior.FLOATING,
        bgcolor=ColorPalette.RED if is_error else ColorPalette.GREEN
    )

    page.show_dialog(notif)
