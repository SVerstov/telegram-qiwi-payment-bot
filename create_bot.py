import logging
import os
import types

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from dotenv import load_dotenv

from middlewares.block_user import BlockUserMiddleware
from settings import WEBHOOK_HOST, WEBHOOK_PATH, WEBAPP_HOST, USE_POOLING, DEBUG
load_dotenv()

TOKEN = os.getenv('API_TOKEN')

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
bot.parse_mode = 'HTML'
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(BlockUserMiddleware())

def launch_bot():
    if USE_POOLING:
        from aiogram.utils import executor
        executor.start_polling(dp, on_startup=on_startup)
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




async def on_startup(dp):
    if DEBUG:
        logging.warning('Starting bot in debug mode')
    if not USE_POOLING:
        await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
