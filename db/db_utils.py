import logging

from db.db_connect import session
from db.models import User, Payments
from aiogram.types import Message


def get_user_by_id(telegram_id: int) -> User:
    return session.query(User).filter_by(telegram_id=telegram_id).first()


def get_payment_by_qiwi_id(bill_id: str) -> Payments:
    return session.query(Payments).filter_by(qiwi_id=bill_id).first()


def add_new_user(message: Message) -> User:
    telegram_id = message.from_user.id
    username = message.from_user.username
    new_user = User(telegram_id=telegram_id, username=username)
    session.add(new_user)
    session.commit()
    logging.info(f'Зарегистрирован новый пользователь {telegram_id} {username}')
    return new_user


def get_or_create_user(message: Message) -> User:
    user = get_user_by_id(telegram_id=message.from_user.id)
    if not user:
        user = add_new_user(message)
    return user
