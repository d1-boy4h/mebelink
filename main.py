import subprocess
import sys
import argparse
from rich import print

from src import App

__author__ = 'd1_boy4h'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='debug mode with mypy & pytest'
    )

    args = parser.parse_args()
    if getattr(args, 'debug', False):
        commands = [
            (['mypy', '.',], 'Проверка типов mypy'),
            (['pytest', '-v'], 'unit-тестирование')
        ]

        for cmd, desc in commands:
            print(f':: [bold blue]{desc}...[/]')
            code = subprocess.run(cmd).returncode
            if code == 5: continue # Игнорирование ошибки об отсутствии тестов
            if code >= 1:
                sys.exit(1)

    app = App()
    app.run()
