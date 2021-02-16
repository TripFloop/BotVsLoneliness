import time

import emoji
from aiogram import types
from aiogram.types import CallbackQuery
from filters import Sasha, Leila
from keyboards.inline.film_inline_keyboard import get_better_pages_keyboard_films
from keyboards.inline.item_delete_inline_keyboard import delete_keyboard
from keyboards.inline.text_inline_keyboard import pagination_call
from keyboards.inline.voice_inline_keyboard import get_better_pages_keyboard_voice, show_voice_message
from loader import dp, bot, db


@dp.message_handler(Sasha(), text=emoji.emojize(":package: Послушай что она там наговорила"))
async def get_voice_message_for_sasha(message: types.Message):
    owner = "sasha"
    try:
        voice = db.get_rand_voice_message(owner='leila')
        if db.check_voice_avaliable(owner=owner, time_trigger=time.time()):
            await bot.send_voice(chat_id=message.chat.id, voice=voice[0])
            db.set_cooldown(owner=owner, time_trigger=time.time())
        else:
            delta = int(db.return_delta(owner=owner, time_trigger=time.time()))
            delta = 3600 - delta
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
            await bot.send_voice(chat_id=message.chat.id, voice=voice[0])
            db.set_cooldown(owner=owner, time_trigger=time.time())
        else:
            delta = int(db.return_delta(owner=owner, time_trigger=time.time()))
            delta = 3600 - delta
            text=f"Прости, но твой час еще не прошел\nТебе осталось еще {delta} секунд\n\nПотерпи, зайка:3"
            await bot.send_message(chat_id=message.chat.id,
                                   text=text)
    except TypeError:
        await message.answer(text="Прости, но голосовых сообщений еще нет")


@dp.message_handler(Leila(), text=emoji.emojize(emoji.emojize(":headphone: Меню голосовых сообщений")))
async def show_voice_menu_leila(message: types.Message):
    owner = "leila"
    await message.answer("Вот твой список гсок",
                         reply_markup=get_better_pages_keyboard_voice(db.get_slice_of_voice_messages(owner), owner))


@dp.message_handler(Sasha(), text=emoji.emojize(emoji.emojize(":headphone: Меню голосовых сообщений")))
async def show_voice_menu_leila(message: types.Message):
    owner = "sasha"
    await message.answer("Вот твой список гсок",
                         reply_markup=get_better_pages_keyboard_voice(db.get_slice_of_voice_messages(owner), owner))


@dp.callback_query_handler(Leila(), pagination_call.filter(key="voice_messages"))
async def show_chosen_page_leila(call: CallbackQuery, callback_data: dict):
    await call.answer()
    owner = "leila"
    current_page = int(callback_data.get("page"))
    markup = get_better_pages_keyboard_voice(db.get_slice_of_voice_messages(owner, current_page),
                                             owner,
                                             page=current_page)
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(Sasha(), pagination_call.filter(key="voice_messages"))
async def show_chosen_page_sasha(call: CallbackQuery, callback_data: dict):
    await call.answer()
    owner = "sasha"
    current_page = int(callback_data.get("page"))
    markup = get_better_pages_keyboard_voice(db.get_slice_of_voice_messages(owner, current_page),
                                             owner,
                                             page=current_page)
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(Leila(), show_voice_message.filter())
async def show_chosen_voice_message(call: CallbackQuery, callback_data: dict):
    await call.answer()
    owner = "leila"
    voice_message_id = int(callback_data.get("voice_message_id"))
    file_id, comment = db.get_voice_message(voice_message_id=voice_message_id, owner=owner)
    await call.message.answer_voice(voice=file_id,
                                    caption=f"{comment}",
                                    reply_markup=delete_keyboard(item_category="voice_messages",
                                                                 owner=owner,
                                                                 item_id=voice_message_id)[0])


@dp.callback_query_handler(Sasha(), show_voice_message.filter())
async def show_chosen_voice_message(call: CallbackQuery, callback_data: dict):
    await call.answer()
    owner = "sasha"
    voice_message_id = int(callback_data.get("voice_message_id"))
    file_id, comment = db.get_voice_message(voice_message_id=voice_message_id, owner=owner)
    await call.message.answer_voice(voice=file_id,
                                    caption=f"{comment}",
                                    reply_markup=delete_keyboard(item_category="voice_messages",
                                                                 owner=owner,
                                                                 item_id=voice_message_id)[0])
