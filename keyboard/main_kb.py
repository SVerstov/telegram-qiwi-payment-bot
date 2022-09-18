from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(
    KeyboardButton('/start'),
    KeyboardButton('/admin'),
            )