import logging

from settings import ADMINS, logs_dir


def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def validate_admin(telegram_id):
    if telegram_id in ADMINS:
        return True
    else:
        logging.warning(f'Пользователь {telegram_id} ломился в аминку. Не пустили')
        return False


def get_logs_list():
    return [f for f in logs_dir.iterdir() if f.is_file()]


