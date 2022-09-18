from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from create_bot import dp, bot
from aiogram import types

from db.db_utils import get_or_create_user, get_all_users, get_user_by_id, add_value_to_balance, block_user, \
    unblock_user, make_balance_info, make_block_list, make_unblock_list
from keyboard.admin_kb import admin_kb, AdminAction
from utils import validate_admin, get_logs_list, is_number


class AdminState(StatesGroup):
    admin_panel_allowed = State()
    changing_balance_wait_id = State()
    changing_balance_wait_value = State()
    block_user_wait_id = State()


@dp.message_handler(commands=['admin'], state='*')
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
    await bot.send_message(chat_id, 'Выгружаю логи...')
    for log in log_list:
        await bot.send_document(chat_id, open(log, 'rb'))
    await callback.answer()
    await AdminState.admin_panel_allowed.set()


@dp.callback_query_handler(text=AdminAction.get_balance, state=AdminState.states)
async def get_balance(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    users = get_all_users()
    msg = make_balance_info(users)
    await bot.send_message(chat_id, msg,)
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
        await bot.send_message(chat_id, 'Пользователь не найден!')


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


@dp.callback_query_handler(text=[AdminAction.block_user, AdminAction.unblock_user], state=AdminState.states)
async def show_block_unblock_cmd(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    if callback.data == AdminAction.block_user:
        msg = make_block_list()
    else:
        msg = make_unblock_list()
    await bot.send_message(chat_id, msg)
    await AdminState.block_user_wait_id.set()
    await callback.answer()



@dp.message_handler(Text(startswith=('/block_','/unblock_')), state=AdminState.states)
async def block_user_cmd(message: types.Message, state: FSMContext):
    if message.text.startswith('/block_'):
        block_unblock_func = block_user
    else:
        block_unblock_func = unblock_user

    user_id = message.text.lstrip('/block_').lstrip('/unblock_')
    if is_number(user_id):
        user_id = int(user_id)
    else:
        await message.answer('Ошибка в id пользователя')
        return
    user = get_user_by_id(user_id)
    if not user:
        msg = 'Пользователь не найден'
    else:
        msg = block_unblock_func(user)
    await message.answer(msg)
    await AdminState.admin_panel_allowed.set()
