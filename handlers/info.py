import logging

from create_bot import dp
from aiogram import types

from db.db_utils import get_or_create_user
from keyboard.payments_kb import new_payment_keyboard


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        username = message.from_user.first_name
        await message.answer(f"Привет, {username}!\n"
                             f"Я - бот для пополнения баланса.\n"
                             f"Нажмите на кнопку, чтобы пополнить баланc.",
                             reply_markup=new_payment_keyboard)
        get_or_create_user(message)