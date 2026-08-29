import sys

from src import App

__author__ = 'd1_boy4h'

if __name__ == '__main__':
    is_debug = False

    if len(sys.argv) > 0:
        import argparse
        import subprocess

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help='debug mode with mypy, ruff and pytest checks'
        )
        parser.add_argument(
            '-b', '--build',
            action='store_true',
            help='build app to apk for android'
        )

        args = parser.parse_args()

        if getattr(args, 'build', False):
            subprocess.run(['flet', 'build', 'apk'], check=False)
            sys.exit()

        elif getattr(args, 'debug', False):
            is_debug = True

            from rich import print as rich_print

            commands = [
                (['mypy', '.',], 'Проверка типов mypy'),
                (['ruff', 'check',], 'Линтинг и форматинг Ruff'),

                # TODO: Расписать тесты остальных репозиториев
                # (['pytest', '-v'], 'unit-тестирование')
            ]

            for cmd, desc in commands:
                rich_print(f':: [bold blue]{desc}...[/]')
                process = subprocess.run(cmd, check=False)
                if process.returncode == 5: continue # Код отсутствия тестов
                elif process.returncode >= 1:
                    sys.exit(1)

    app = App(is_debug)
    app.run()

# TODO-лист

#* Разделы (фронт)
# Переименование раздела
# Удаление раздела

#* Тудушки (фронт)
# Создание тудушки
# Отображение тудушек внутри раздела
# Выполнение тудушки
# Тултип с меню при зажатии тудушки
# Редактирование тудушки
# Удаление раздела

#* Заметки проекта (фронт и бэк)
# Debounce-декоратор
# CRUD
