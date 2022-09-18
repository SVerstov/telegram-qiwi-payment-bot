from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update

from db import blacklist


class BlockUserMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: Update, data: dict):
        user_id = None
        if update.callback_query:
            user_id = update.callback_query.from_user.id
        elif update.message:
            user_id = update.message.from_user.id
        if user_id in blacklist:
            raise CancelHandler()
