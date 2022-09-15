import logging

from create_bot import dp
from aiogram import types
import logging


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    username = message.from_user.first_name
    await message.answer(f'Привет, {username}')  # todo дополнить сообщение + inline



@dp.message_handler(commands=['error'])
async def send_welcome(message: types.Message):
    await message.answer(f'Сейчас будет ошибка')
    logging.error('Error test')