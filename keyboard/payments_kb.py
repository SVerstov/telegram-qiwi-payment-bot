from aiogram import types

new_payment_keyboard= types.InlineKeyboardMarkup(row_width=1)
new_payment_btn = types.InlineKeyboardButton('Пополнить баланс', callback_data='new_payment')
new_payment_keyboard.add(new_payment_btn)


