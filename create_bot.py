import logging
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from dotenv import load_dotenv

from settings import WEBHOOK_HOST, WEBHOOK_PATH, WEBAPP_HOST, USE_POOLING, DEBUG
load_dotenv()

TOKEN = os.getenv('API_TOKEN')

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def launch_bot():
    if USE_POOLING:
        from aiogram.utils import executor
        executor.start_polling(dp)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=5000,
        )

    if DEBUG:
        logging.warning('Starting bot in debug mode')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
