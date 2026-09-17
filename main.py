import sys
import tomllib
from pathlib import Path

from src import App
from src.constants import MetaInfo

__author__  = MetaInfo.AUTHOR
__version__ = MetaInfo.VERSION

def sync_version():
    '''Синхронизация версии в pyproject.toml с MetaInfo.VERSION.'''

    import subprocess

    from rich import print as rich_print

    pyproject_path = Path('pyproject.toml')

    if not pyproject_path.exists():
        return

    try:
        with pyproject_path.open('rb') as f:
            data = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as e:
        rich_print(
            f':: [bold red]Не удалось прочитать pyproject.toml: {e}[/]'
        )

        return

    current_version = data.get('project', {}).get('version')
    if current_version == MetaInfo.VERSION:
        return

    rich_print(
        f':: [bold blue]Синхронизация версии: {current_version} → {MetaInfo.VERSION}[/]'
    )

    try:
        subprocess.run(
            ['uv', 'version', MetaInfo.VERSION],
            check=True,
            capture_output=True,
            text=True
        )

        rich_print(f':: [bold green]Версия обновлена до {MetaInfo.VERSION}[/]')

    except subprocess.CalledProcessError as e:
        rich_print(
            f'[bold red]uv version завершился с ошибкой: {e.stderr}[/]',
            file=sys.stderr
        )

if __name__ == '__main__':
    is_debug = False

    if len(sys.argv) > 1:
        sync_version()

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
