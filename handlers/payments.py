import logging

from create_bot import dp, bot
from aiogram import types
from keyboard.payments_kb import new_payment_keyboard


@dp.callback_query_handler(text='new_payment')
async def new_payment(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, 'оп!')
    await callback_query.answer()
 