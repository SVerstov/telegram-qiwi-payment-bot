import logging
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('API_TOKEN')

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')
DEBUG = os.getenv('DEBUG') == 'True'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def launch_bot():
    if DEBUG:
        from aiogram.utils import executor
        print('Start bot in debug mode')  # todo переделать в лог
        executor.start_polling(dp)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
