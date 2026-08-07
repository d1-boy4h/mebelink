import argparse
import subprocess
import sys

from rich import print

from src import App

__author__ = 'd1_boy4h'

if __name__ == '__main__':
    is_debug = False

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='debug mode with mypy & pytest'
    )

    args = parser.parse_args()
    if getattr(args, 'debug', False):
        is_debug = True
        commands = [
            (['mypy', '.',], 'Проверка типов mypy'),
            (['ruff', 'check',], 'Линтинг и форматинг Ruff'),
            (['pytest', '-v'], 'unit-тестирование')
        ]

        for cmd, desc in commands:
            print(f':: [bold blue]{desc}...[/]')
            code = subprocess.run(cmd, check=False).returncode
            if code == 5: continue # Игнорирование ошибки об отсутствии тестов
            if code >= 1:
                sys.exit(1)

    app = App(is_debug)
    app.run()

# TODO-лист

# Исправить повторные файлы
# Просмотр файлов
# Удаление файлов

# Тудушки
# Сделать авто удаление логов по дням и по количеству строк
# Закомментить дебаг-систему в этом файле
