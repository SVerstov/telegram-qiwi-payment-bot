import logging
from pathlib import Path
from typing import Literal
from settings import info_log_file, warnings_log_file, console_log_level, log_format


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
    info_handler = get_logger_handler(log_file=info_log_file, level=logging.INFO)
    warning_handler = get_logger_handler(log_file=warnings_log_file, level=logging.WARNING)
    console_handler = get_logger_handler(console_handler=True, level=console_log_level)

    logging.basicConfig(level=logging.DEBUG, format=log_format, handlers=[info_handler,
                                                                          warning_handler,
                                                                          console_handler])
