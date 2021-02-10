from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import owner_id, Leila_id


class Sasha(BoundFilter):

    async def check(self, message: types.Message):
        return message.from_user.id == owner_id


class Leila(BoundFilter):

    async def check(self, message: types.Message):
        return message.from_user.id == Leila_id

