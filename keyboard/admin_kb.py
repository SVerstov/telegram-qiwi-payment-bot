from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_kb = InlineKeyboardMarkup(row_width=2)


class AdminAction:
    get_logs = 'admin:get_logs'
    get_balance = 'admin:get_balance'
    change_balance = 'admin:change_balance'
    block_user = 'admin:block_user'
    unblock_user = 'admin:unblock_user'


btn1 = InlineKeyboardButton('Выгрузить логи', callback_data=AdminAction.get_logs)
btn2 = InlineKeyboardButton('Выгрузить баланс', callback_data=AdminAction.get_balance)
btn3 = InlineKeyboardButton('Изменить баланс пользователя', callback_data=AdminAction.change_balance)
btn4 = InlineKeyboardButton('Забанить пользователя', callback_data=AdminAction.block_user)
btn5 = InlineKeyboardButton('Разбанить пользователя', callback_data=AdminAction.unblock_user)
admin_kb.row(btn1, btn2).add(btn3).add(btn4).add(btn5)
