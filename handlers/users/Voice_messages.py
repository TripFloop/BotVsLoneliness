import emoji
from aiogram import types

from filters import Sasha, Leila
from loader import dp, bot, db
from utils.misc import rate_limit
from utils.misc.one_time_per_period import Datetime


@dp.message_handler(Sasha(), text=emoji.emojize(":package: Послушай что она там наговорила"))
async def get_voice_message_for_sasha(message: types.Message):
    try:
        await bot.send_voice(chat_id=message.chat.id, voice=db.get_rand_voice_message(owner='leila'))
        db.
    except TypeError:
        await message.answer(text="Прости, но голосовых сообщений еще нет")


@dp.message_handler(Leila(), text=emoji.emojize(":package: Послушай что он там наговорил :3"))
async def get_voice_message_for_leila(message: types.Message):
    try:
        await bot.send_voice(chat_id=message.chat.id, voice=db.get_rand_voice_message(owner='sasha'))
    except TypeError:
        await message.answer(text="Прости, но голосовых сообщений еще нет")
