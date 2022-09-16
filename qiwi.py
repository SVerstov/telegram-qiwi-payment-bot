import logging
import os

from dotenv import load_dotenv
from pyqiwip2p import AioQiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime, Bill

from db.db_connect import session
from db.db_utils import get_user_by_id, get_payment_by_qiwi_id
from db.models import Payments

load_dotenv()

QIWI_PRIV_KEY = os.getenv('QIWI_PRIV_KEY')
p2p = AioQiwiP2P(auth_key=QIWI_PRIV_KEY)


async def create_bill(telegram_id: int, amount: int) -> Bill:
    new_bill = await p2p.bill(amount=amount, lifetime=5)
    _save_payment_into_db(telegram_id, amount, new_bill.bill_id)
    return new_bill


def _save_payment_into_db(telegram_id: int, amount: int, qiwi_id: str, ) -> None:
    new_payment = Payments(telegram_id=telegram_id, qiwi_id=qiwi_id, amount=amount)
    session.add(new_payment)
    session.commit()
    logging.info(f'Создан новый счет {new_payment}')


async def check_payment(bill_id: str) -> bool:
    bill = await p2p.check(bill_id=bill_id)
    if bill.status == 'PAID':
        return True
    return False


balance = int


def increase_user_balance(telegram_id: int, bill_id: str) -> balance:
    """save balance into DB and return current balance"""
    user = get_user_by_id(telegram_id=telegram_id)
    payment = get_payment_by_qiwi_id(bill_id)
    if payment.telegram_id == user.telegram_id and payment.is_completed is False:
        user.balance += payment.amount
        payment.is_completed = True
        session.commit()
        logging.info(f'{user} зачислено {payment.amount}. Баланс={user.balance}')
    return user.balance
