from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyqiwip2p.p2p_types import Bill

new_payment_keyboard = InlineKeyboardMarkup(row_width=1)
new_payment_btn = InlineKeyboardButton('Пополнить баланс', callback_data='new_payment')
new_payment_keyboard.add(new_payment_btn)


checker_prefix = 'pay_checker:'

def make_url_and_check_kb(bill: Bill) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    url_btn = InlineKeyboardButton('Произвести оплату 💶', url=bill.pay_url)
    callback = f'{checker_prefix}{bill.bill_id}'
    check_btn = InlineKeyboardButton('Проверить платёж ☑️', callback_data=callback)
    kb.add(url_btn, check_btn)
    return kb
