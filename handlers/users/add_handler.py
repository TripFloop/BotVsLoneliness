from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from data.config import owner_id, leila_id
from filters import Leila, Sasha
from handlers.users.music_handler import music_mood_add
from handlers.users.pics_handler import show_pics_menu_sasha, show_pics_menu_leila
from handlers.users.text_handler import show_text_menu_sasha, show_text_menu_leila
from keyboards.inline.add_item_inline_keyboard import add_cb
from keyboards.inline.back_button_inline_keyboard import back_button_keyboard, func_cb
from keyboards.inline.iserotic_inline_keyboard import iserotic_keyboard, iserotic_keyboard_leila
from loader import dp, db, bot
from states import MenuStates


@dp.callback_query_handler(add_cb.filter())
async def add_item_menu(call: CallbackQuery, callback_data: dict):
    item_category = callback_data.get("item_category")
    if item_category == "music":
        await music_mood_add(call)
        return True  # kludge
    text = "Добавь то, что хочешь"
    if item_category == "voice_message":
        text = "Скажи то, что хочешь"
    await call.answer()
    markup = back_button_keyboard(prev_func=item_category)
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    await MenuStates.add.set()
    if item_category == "text":
        await MenuStates.add_text.set()
    if item_category == "films":
        await MenuStates.add_film.set()


@dp.callback_query_handler(func_cb.filter(), state=MenuStates.add)
async def back_to_func(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
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
    data = await state.get_data("voice_id")
    voice_id = data.get("voice_id")
    db.add_voice_message(owner="leila", file_id=voice_id, comment=message.text)
    await message.answer(text="Ты успешно записала гску")
    await state.finish()


@dp.message_handler(Sasha(), state=MenuStates.voice_comment)
async def add_to_db_voice_message(message: types.Message, state: FSMContext):
    data = await state.get_data("voice_id")
    voice_id = data.get("voice_id")
    db.add_voice_message(owner="sasha", file_id=voice_id, comment=message.text)
    await message.answer(text="Только не слушай больше это убожество, пожалуйста")
    await state.finish()


@dp.message_handler(Leila(), state=MenuStates.add, content_types=ContentType.AUDIO)
async def add_to_db_music(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.audio.file_id, music_name=message.audio.file_name,
                            duration=message.audio.duration)


@dp.message_handler(Sasha(), state=MenuStates.add, content_types=ContentType.PHOTO)
async def got_photo_sasha(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    owner = "sasha"
    await state.update_data({"file_id": file_id, "owner": owner})
    await message.answer("Твоя картинка эро или нет?", reply_markup=iserotic_keyboard())
    await MenuStates.iserotic_pic.set()


@dp.message_handler(Leila(), state=MenuStates.add, content_types=ContentType.PHOTO)
async def got_photo_leila(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    owner = "leila"
    await state.update_data({"file_id": file_id, "owner": owner})
    await message.answer("Твоя картинка - эротическая или милая вкуснота? :3", reply_markup=iserotic_keyboard_leila())
    await MenuStates.iserotic_pic.set()


@dp.callback_query_handler(state=MenuStates.iserotic_pic)
async def added_to_db_pic(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    file_id = state_data.get("file_id")
    owner = state_data.get("owner")
    iserotic = call.data[9:]
    if iserotic == "False":
        iserotic = False
    else:
        iserotic = True
    db.add_pic(owner, file_id, iserotic)
    await call.answer("Картинка добавлена")
    if call.message.from_user.id == owner_id:
        await show_pics_menu_sasha(call.message)
    elif call.message.from_user.id == leila_id:
        await show_pics_menu_leila(call.message)
    await state.finish()


@dp.message_handler(state=MenuStates.add_text)
async def erotic_or_not_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data({"text": text})
    await message.answer("Твой текст эротический или милый?", reply_markup=iserotic_keyboard_leila())
    await MenuStates.iserotic_text.set()


@dp.callback_query_handler(Sasha(), state=MenuStates.iserotic_text)
async def add_text_to_db(call: CallbackQuery, state: FSMContext):
    iserotic = call.data[9:]
    if iserotic == "False":
        iserotic = False
    else:
        iserotic = True
    data = await state.get_data()
    text = data.get("text")
    owner = "sasha"
    db.add_text(text, owner, iserotic)
    await call.answer("Текст был успешно добавлен")
    await show_text_menu_sasha(call.message)
    await state.finish()


@dp.callback_query_handler(Leila(), state=MenuStates.iserotic_text)
async def add_text_to_db(call: CallbackQuery, state: FSMContext):
    iserotic = call.data[9:]
    if iserotic == "False":
        iserotic = False
    else:
        iserotic = True
    data = await state.get_data()
    text = data.get("text")
    owner = "leila"
    db.add_text(text, owner, iserotic)
    await call.answer("Текст был успешно добавлен\nЖду, когда он его увидит, ты его приятно порадуешь :3")
    await show_text_menu_leila(call.message)
    await state.finish()


@dp.message_handler(state=MenuStates.add_film)
async def add_comment(message: types.Message, state: FSMContext):
    film_name = message.text
    await state.update_data({"film_name": film_name})
    await message.answer("Напиши небольшой комментарий\nНапример приоритет или еще что-то")
    await MenuStates.add_comment.set()


@dp.message_handler(state=MenuStates.add_comment)
async def add_film_to_db(message: types.Message, state: FSMContext):
    data_dict = await state.get_data()
    film_name = data_dict.get("film_name")
    comment = message.text
    db.add_film(film_name, comment)
    await message.answer("Тайтл был успешно добавлен")
    await state.finish()

# @dp.message_handler(Leila(), state=MenuStates.add, content_types=ContentType.PHOTO)
# async def


# @dp.callback_query_handler(Leila(), iserotic_cb.filter())
# async def after_iserotic_question_add_pic(call: CallbackQuery, callback_data: dict):


# (text=emoji.emojize(":paw_prints: Это эротика? :3"), reply_markup = iserotic_markup)
