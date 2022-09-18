import logging

from db.db_connect import db_session
from db.models import User, Payments
from aiogram.types import Message
from db import blacklist


def get_user_by_id(telegram_id: int) -> User:
    return db_session.query(User).filter_by(telegram_id=telegram_id).first()


def get_payment_by_qiwi_id(bill_id: str) -> Payments:
    return db_session.query(Payments).filter_by(qiwi_id=bill_id).first()


def add_new_user(message: Message) -> User:
    telegram_id = message.from_user.id
    username = message.from_user.username
    new_user = User(telegram_id=telegram_id, username=username)
    db_session.add(new_user)
    db_session.commit()
    logging.info(f'Зарегистрирован новый пользователь {telegram_id} {username}')
    return new_user


def get_or_create_user(message: Message) -> User:
    user = get_user_by_id(telegram_id=message.from_user.id)
    if not user:
        user = add_new_user(message)
    return user


def get_all_users() -> list[User]:
    return db_session.query(User).all()


balance = int


def add_value_to_balance(user: User, value: int) -> balance:
    old_balance = user.balance
    user.balance += value
    db_session.commit()
    logging.info(f'Ручное изменение баланса! {user}: {old_balance}+{value}={user.balance} ')
    return user.balance


log_msg = str


def block_user(user: User) -> log_msg:
    if user.is_blocked:
        log_msg = f'{user} Уже забанен'
    else:
        user.is_blocked = True
        blacklist.add(user.telegram_id)
        log_msg = f'{user} забанен'
        db_session.commit()
        logging.info(log_msg)
    return log_msg


def unblock_user(user: User) -> log_msg:
    log_msg = f'{user} разбанен'

    if user.is_blocked:
        user.is_blocked = False
        try:
            blacklist.remove(user.telegram_id)
        except KeyError:
            update_blacklist()
            logging.exception('Неверная работа функции unblock_user')

        db_session.commit()
        logging.info(log_msg)
    return log_msg


def update_blacklist():
    blacklist.clear()
    block_users = db_session.query(User).filter(User.is_blocked).all()
    if block_users:
        for user in block_users:
            blacklist.add(user.telegram_id)


def make_balance_info(users: list[User]) -> str:
    info = '<b>Telegram id / username / balance</b>\n'
    for user in users:
        info += f'\n{user.telegram_id} / {user.username} / {user.balance}'
    return info


def _make_block_unblock_cmd_and_info(show_block_cmds: bool = False) -> str:
    info = 'Выберите пользователя:'
    users = db_session.query(User).filter(User.is_blocked != show_block_cmds).all()
    cmd = '/block_' if show_block_cmds else '/unblock_'
    for user in users:
        info += f'\n{cmd}{user.telegram_id} / {user.username} / Баланс = {user.balance}'
    return info


def make_block_list() -> str:
    return _make_block_unblock_cmd_and_info(show_block_cmds=True)


def make_unblock_list() -> str:
    return _make_block_unblock_cmd_and_info(show_block_cmds=False)
