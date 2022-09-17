import logging
from pathlib import Path
from typing import Literal
from settings import console_log_level, log_format, logs_dir


def get_logger_handler(log_file: Path = None,
                       console_handler=False,
                       level: Literal[10, 20, 30, 40, 50] = logging.INFO
                       ) -> logging.FileHandler | logging.StreamHandler:
    formatter = logging.Formatter(log_format)

    if console_handler or log_file is None:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler(log_file, encoding='utf-8')

    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler




def setup_logger():
    _check_log_dir()
    info_handler = get_logger_handler(log_file=Path(logs_dir,'info.log'), level=logging.INFO)
    warning_handler = get_logger_handler(log_file=Path(logs_dir,'warnings.log'), level=logging.WARNING)
    console_handler = get_logger_handler(console_handler=True, level=console_log_level)

    logging.basicConfig(level=logging.DEBUG, format=log_format, handlers=[info_handler,
                                                                          warning_handler,
                                                                          console_handler])


def _check_log_dir():
    if not logs_dir.is_dir():
        Path.mkdir(logs_dir)
