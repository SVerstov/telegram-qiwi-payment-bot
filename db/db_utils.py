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


def block_unblock_user(user: User) -> log_msg:
    user.is_blocked = not user.is_blocked
    if user.is_blocked:
        log_msg = f'{user} Забанен'
        blacklist.add(user.telegram_id)
    else:
        log_msg = f'{user} Разбанен'
        try:
            blacklist.remove(user.telegram_id)
        except KeyError:
            update_blacklist()

    db_session.commit()
    logging.info(log_msg)
    return log_msg


def update_blacklist():
    blacklist.clear()
    block_users = db_session.query(User).filter(User.is_blocked is True).all()
    if block_users:
        for user in block_users:
            blacklist.add(user.telegram_id)
