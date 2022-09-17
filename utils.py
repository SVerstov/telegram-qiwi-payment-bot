import logging

from db.models import User
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


def make_balance_info(users: list[User]) -> str:
    info = 'Telegram id / username / balance'
    for user in users:
        info += f'\n{user.telegram_id} / {user.username} / {user.balance}'
    return info


