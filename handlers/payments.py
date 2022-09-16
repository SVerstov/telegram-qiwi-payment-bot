from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from create_bot import dp, bot
from aiogram import types

from keyboard.payments_kb import make_url_and_check_kb, checker_prefix
from qiwi import create_bill, check_payment, increase_user_balance
from utils import is_number


class PaymentsState(StatesGroup):
    enter_value = State()


@dp.callback_query_handler(text='new_payment')
async def new_payment(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, 'Введите сумму, на которую вы хотите пополнить баланс:')
    await PaymentsState.enter_value.set()
    await callback_query.answer()


@dp.message_handler(state=PaymentsState.enter_value)
async def enter_value(message: types.Message, state: FSMContext):
    pass
    if not is_number(message.text):
        await message.reply('Введите число!')
    else:
        amount = abs(int(message.text))
        bill = await create_bill(telegram_id=message.from_user.id, amount=amount)
        kb = make_url_and_check_kb(bill)
        await message.answer('Счёт создан!',reply_markup=kb)
        await state.finish()


@dp.callback_query_handler(Text(startswith=checker_prefix))
async def pay_checker(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    bill_id = callback_query.data.lstrip(checker_prefix)
    if await check_payment(bill_id):
        balance = increase_user_balance(telegram_id=chat_id, bill_id=bill_id)
        await bot.send_message(chat_id, f'Платёж прошёл. Ваш баланс={balance}')
    else:
        await bot.send_message(chat_id, 'Платёж не прошёл 😣')
    await callback_query.answer()

