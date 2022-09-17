# bot.restrict_chat_member(chat_id, chat_id, can_send_messages=False)

import logging

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from create_bot import dp, bot
from aiogram import types

from db.db_utils import get_or_create_user, get_all_users, get_user_by_id, add_value_to_balance, block_user
from keyboard.admin_kb import admin_kb, AdminAction
from utils import validate_admin, get_logs_list, make_balance_info, is_number


class AdminState(StatesGroup):
    admin_panel_allowed = State()
    changing_balance_wait_id = State()
    changing_balance_wait_value = State()
    block_user_wait_id = State()


@dp.message_handler(commands=['admin'])
async def show_admin_panel(message: types.Message):
    if message.chat.type == 'private':
        if validate_admin(message.from_user.id):
            await message.answer(f"Добро пожаловать в админку!\n", reply_markup=admin_kb)
            await AdminState.admin_panel_allowed.set()
        else:
            await message.answer(f"Доступ запрещён!\n")
        get_or_create_user(message)
    

@dp.callback_query_handler(text=AdminAction.get_logs, state=AdminState.states)
async def get_logs(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id

    log_list = get_logs_list()
    for log in log_list:
        await bot.send_document(chat_id, open(log, 'rb'))
    await callback.answer()
    await AdminState.admin_panel_allowed.set()


@dp.callback_query_handler(text=AdminAction.get_balance, state=AdminState.states)
async def get_balance(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    users = get_all_users()
    msg = make_balance_info(users)
    await bot.send_message(chat_id, msg)
    await callback.answer()
    await AdminState.admin_panel_allowed.set()


@dp.callback_query_handler(text=AdminAction.change_balance, state=AdminState.states)
async def pre_change_balance(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    await bot.send_message(chat_id, 'Введите id пользователя, которому вы хотите поменять баланс:')
    await AdminState.changing_balance_wait_id.set()
    await callback.answer()


@dp.message_handler(state=AdminState.changing_balance_wait_id)
async def change_balance_enter_id(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id

    editable_user = get_user_by_id(message.text)
    if editable_user:
        msg = f'{editable_user} баланс={editable_user.balance}\n' \
              f'Введите число, на которое будет изменён баланс:'
        await bot.send_message(chat_id, msg)
        await AdminState.changing_balance_wait_value.set()
        await state.update_data(editable_user_id=editable_user.telegram_id)
    else:
        await bot.send_message(chat_id, 'Введите число, на которое будет изменён баланс:')


@dp.message_handler(state=AdminState.changing_balance_wait_value)
async def change_balance_enter_value(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id

    if not is_number(message.text):
        await bot.send_message(chat_id, 'Введите число')
        return

    delta = int(message.text)
    data = await state.get_data()
    editable_user = get_user_by_id(data.get('editable_user_id'))
    add_value_to_balance(editable_user, int(delta))
    msg = f'Баланс изменён!\n' \
          f'{editable_user} баланс={editable_user.balance}'
    await bot.send_message(chat_id, msg)
    await AdminState.admin_panel_allowed.set()


@dp.callback_query_handler(text=AdminAction.block_user, state=AdminState.states)
async def block_user_enter_name(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    await bot.send_message(chat_id, 'Введите id пользователя, который будет забанен/разбанен')
    await AdminState.block_user_wait_id.set()
    await callback.answer()


@dp.message_handler(state=AdminState.block_user_wait_id)
async def block_user_enter_id(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    user = get_user_by_id(message.text)
    if not user:
        msg = 'Пользователь не найден'
    else:
        msg = block_user(user)

    await bot.send_message(chat_id, msg)
    await AdminState.admin_panel_allowed.set()

