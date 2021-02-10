from pprint import pprint

import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, InlineKeyboardMarkup, InlineKeyboardButton

from filters import Leila, Sasha
from keyboards.inline.add_item_inline_keyboard import add_cb
from keyboards.inline.iserotic_inline_keyboard import iserotic_cb, iserotic_markup
from keyboards.inline.text_inline_keyboard import get_better_pages_keyboard
from loader import dp, db, bot
from states import MenuStates
from keyboards.inline.back_button_inline_keyboard import back_button_keyboard, func_cb


@dp.callback_query_handler(add_cb.filter())
async def add_item_menu(call: CallbackQuery, callback_data: dict):
    item_category = callback_data.get("item_category")
    text = 'Добавь то, что хочешь'
    if item_category == 'voice_message':
        text = 'Скажи то, что хочешь'
    await call.answer()
    markup = back_button_keyboard(prev_func=item_category)
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    await MenuStates.add.set()


@dp.callback_query_handler(Leila(), func_cb.filter(), state=MenuStates.add)
async def back_to_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    prev_func = callback_data.get("prev_func")
    if prev_func == "text":
        await bot.send_message(chat_id=call.message.chat.id, text="""
                                             Привет, вот твой список текстов, выбирай, что нужно
                                             """, reply_markup=get_better_pages_keyboard(db.get_all_text(owner='leila'),
                                                                                         owner='leila'))
    # elif prev_func == "films":
    #     await show_films_menu_leila()
    # elif prev_func == "voice_messages":
    #     await show_voice_messages_menu_leila()
    # elif prev_func == "pics":
    #     await show_pics_menu_leila()
    await state.finish()


@dp.callback_query_handler(Sasha(), func_cb.filter(), state=MenuStates.add)
async def back_to_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    prev_func = callback_data.get("prev_func")
    if prev_func == "text":
        await bot.send_message(chat_id=call.message.chat.id, text="""
                                             Привет, вот твой список текстов, выбирай, что нужно
                                             """, reply_markup=get_better_pages_keyboard(db.get_all_text(owner='sasha'),
                                                                                         owner='sasha'))
    # elif prev_func == "films":
    #     await show_films_menu_leila()
    # elif prev_func == "voice_messages":
    #     await show_voice_messages_menu_leila()
    # elif prev_func == "pics":
    #     await show_pics_menu_leila()
    await state.finish()


@dp.message_handler(Leila(), state=MenuStates.add, content_types=ContentType.VOICE)
async def add_item(message: types.Message, state: FSMContext):
    voice_id = message.voice.file_id
    await state.update_data(voice_id=voice_id)
    await message.answer(text="Добавь коротенький комментарий\nНе больше 30 символов\nОн нужен для себя любимой")
    await MenuStates.voice_comment.set()


@dp.message_handler(Sasha(), state=MenuStates.add, content_types=ContentType.VOICE)
async def add_item(message: types.Message, state: FSMContext):
    voice_id = message.voice.file_id
    await state.update_data(voice_id=voice_id)
    await message.answer(text="Твой коммент\nДавай-давай")
    await MenuStates.voice_comment.set()


@dp.message_handler(Leila(), state=MenuStates.voice_comment)
async def add_to_db_voice_message(message: types.Message, state: FSMContext):
    voice_id = await state.get_data("voice_id")
    db.add_voice_message(owner="leila", file_id=voice_id, comment=message.text)
    await message.answer(text="Ты успешно записала гску")
    await state.finish()


@dp.message_handler(Sasha(), state=MenuStates.voice_comment)
async def add_to_db_voice_message(message: types.Message, state: FSMContext):
    voice_id = await state.get_data("voice_id")
    db.add_voice_message(owner="sasha", file_id=voice_id, comment=message.text)
    await message.answer(text="Только не слушай больше это убожество, пожалуйста")
    await state.finish()


@dp.message_handler(Leila(), state=MenuStates.add, content_types=ContentType.AUDIO)
async def add_to_db_music(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.audio.file_id, music_name=message.audio.file_name,
                            duration=message.audio.duration)


@dp.callback_query_handler(add_cb.filter(item_category="pics"))
async def ask_add_pic_to_db(call: CallbackQuery, callback_data: dict):
    await call.answer(text="Отправь только одну картинку, несколько бот не будет определять")
    await MenuStates.add.set()


@dp.callback_query_handler(add_cb.filter(item_category="text"))
async def add_text_to_db(call: CallbackQuery):
    pass


@dp.message_handler(Sasha(), content_types=ContentType.PHOTO)
async def first_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    print(file_id)
    await message.answer_photo(file_id)
    db.add_pic(owner="sasha", file_id=file_id, iserotic=1.0)

# @dp.message_handler(Leila(), state=MenuStates.add, content_types=ContentType.PHOTO)
# async def


# @dp.callback_query_handler(Leila(), iserotic_cb.filter())
# async def after_iserotic_question_add_pic(call: CallbackQuery, callback_data: dict):


# (text=emoji.emojize(":paw_prints: Это эротика? :3"), reply_markup = iserotic_markup)
