from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler


class OneTimeMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'one_time_per_limit')
            key = getattr(handler, 'one_time_per_limit')