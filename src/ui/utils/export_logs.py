import logging
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def export_logs(path: str) -> str:
    '''Экспорт логов в архив.'''

    logger = logging.getLogger(__name__)

    valid_path = path
    if not path.endswith('.zip'):
        valid_path = path + '.zip'

    logs_path = Path('logs/')

    try:
        with ZipFile(valid_path, 'w', ZIP_DEFLATED) as zf:
            for log_file in logs_path.iterdir():
                if str(log_file).endswith('.log'):
                    zf.write(log_file, log_file.name)

    except Exception as e:  # noqa: BLE001
        error = RuntimeError(f'Непредвиденная ошибка экспорта: {e}')

        logger.error(error)
        raise error

    return path
