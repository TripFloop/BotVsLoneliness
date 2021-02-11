import emoji
from aiogram import types

from filters import Sasha, Leila
from loader import dp, bot, db
from utils.misc import rate_limit
from utils.misc.one_time_per_period import Datetime
import time


@dp.message_handler(Sasha(), text=emoji.emojize(":package: Послушай что она там наговорила"))
async def get_voice_message_for_sasha(message: types.Message):
    owner = "sasha"
    try:
        voice = db.get_rand_voice_message(owner='leila')
        if db.check_voice_avaliable(owner=owner, time_trigger=time.time()):
            await bot.send_voice(chat_id=message.chat.id, voice=voice)
            db.set_cooldown(owner=owner, time_trigger=time.time())
        else:
            delta = int(db.return_delta(owner=owner, time_trigger=time.time()))
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Прости, но твой час еще не прошел\nТебе осталось еще {delta} секунд")
    except TypeError:
        await message.answer(text="Прости, но голосовых сообщений еще нет")


@dp.message_handler(Leila(), text=emoji.emojize(":package: Послушай что он там наговорил :3"))
async def get_voice_message_for_leila(message: types.Message):
    owner = "leila"
    try:
        voice = db.get_rand_voice_message(owner='sasha')
        if db.check_voice_avaliable(owner=owner, time_trigger=time.time()):
            await bot.send_voice(chat_id=message.chat.id, voice=voice)
            db.set_cooldown(owner=owner, time_trigger=time.time())
        else:
            delta = int(db.return_delta(owner=owner, time_trigger=time.time()))
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"""Прости, но твой час еще не прошел\n
                                            Тебе осталось еще {delta} секунд\n
                                            Потерпи, зайка:3""")
    except TypeError:
        await message.answer(text="Прости, но голосовых сообщений еще нет")
