from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from aiogram.utils import emoji
from data.config import owner_id, leila_id
from filters import Sasha, Leila
from keyboards.inline.add_item_inline_keyboard import add_item_keyboard
from keyboards.inline.item_delete_inline_keyboard import delete_keyboard
from keyboards.inline.mood_type_inline_keyboard import mood_inline, mood_cb
from keyboards.inline.music_inline_keyboard import get_better_pages_keyboard_music, show_track
from keyboards.inline.text_inline_keyboard import pagination_call
from loader import dp, db
from states import MenuStates


@dp.message_handler(Sasha(), text=emoji.emojize(":musical_note: Плейлист"))
async def choose_music_mood_sasha(message: types.Message):
    await message.answer("Выбери то, что хочешь послушать сегодня", reply_markup=mood_inline())


@dp.message_handler(Leila(), text=emoji.emojize(":musical_note: Плейлист"))
async def choose_music_mood_leila(message: types.Message):
    await message.answer("Какое на этот раз у тебя настроение, кися? :3", reply_markup=mood_inline())


@dp.callback_query_handler(Sasha(), mood_cb.filter())
async def show_start_music_sasha(call: CallbackQuery, callback_data: dict):
    mood_type = callback_data.get("mood_type")
    await call.message.edit_text(f"Вот твой список под настроение {mood_type}")
    try:
        await call.message.edit_reply_markup(
            reply_markup=get_better_pages_keyboard_music(sliced_array=db.get_slice_of_music_by_mood(mood_type),
                                                         mood=mood_type))
    except TypeError:
        await call.message.answer("Прости, но пока нет музыки, добавь свою, только давай нормальную",
                                  reply_markup=add_item_keyboard("music")[0])
        await MenuStates.add_music.set()


@dp.callback_query_handler(Leila(), mood_cb.filter())
async def show_start_music_sasha(call: CallbackQuery, callback_data: dict):
    mood_type = callback_data.get("mood_type")
    await call.message.edit_text(f"Вот твой список под настроение {mood_type}")
    try:
        await call.message.edit_reply_markup(
            reply_markup=get_better_pages_keyboard_music(sliced_array=db.get_slice_of_music_by_mood(mood_type),
                                                         mood=mood_type))
    except TypeError:
        await call.message.answer("Прости, но пока нет музыки, добавь свою :3",
                                  reply_markup=add_item_keyboard("music")[0])
        await MenuStates.add_music.set()


@dp.callback_query_handler(pagination_call.filter(page="current_page"))
async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


@dp.callback_query_handler(pagination_call.filter(key="music_calm"))
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer()
    mood = callback_data.get("key")
    current_page = int(callback_data.get("page"))
    mood = mood[6:]  # kludge
    markup = get_better_pages_keyboard_music(db.get_slice_of_music_by_mood(mood=mood, page=current_page), mood=mood,
                                             page=current_page)
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(pagination_call.filter(key="music_happy"))
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer()
    mood = callback_data.get("key")
    current_page = int(callback_data.get("page"))
    mood = mood[6:]  # kludge
    markup = get_better_pages_keyboard_music(db.get_slice_of_music_by_mood(mood=mood, page=current_page), mood=mood,
                                             page=current_page)
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(state=MenuStates.add_music)
async def music_mood_add(call: CallbackQuery):
    await call.message.answer("Выбери настроение своей музыки", reply_markup=mood_inline())
    await MenuStates.add_mood.set()


@dp.callback_query_handler(state=MenuStates.add_mood)
async def music_upload(call: CallbackQuery, state: FSMContext):
    mood_type = call.data[5:]
    await call.message.answer("Пожалуйста, загрузи только один трек, к сожалению очень трудно ловить MediaGroup")
    await state.update_data({"mood": mood_type})
    await MenuStates.add_music.set()


@dp.message_handler(state=MenuStates.add_music, content_types=ContentType.AUDIO)
async def music_uploaded(message: types.Message, state: FSMContext):
    data = await state.get_data()
    mood_type = data.get("mood")
    duration = message.audio.duration
    file_id = message.audio.file_id
    music_name = message.audio.title
    db.add_music(mood_type, file_id, music_name, duration)
    await message.answer("Трек успешно добавлен\nПерекидываю в меню выбора настроения")
    if message.from_user.id == owner_id:
        await choose_music_mood_sasha(message)
    elif message.from_user.id == leila_id:
        await choose_music_mood_leila(message)
    await state.finish()


@dp.callback_query_handler(show_track.filter())
async def show_track(call: CallbackQuery, callback_data: dict):
    music_id = callback_data.get("track_id")
    file_id, duration = db.get_music(music_id)
    await call.message.answer_audio(file_id, duration=duration,
                                    reply_markup=delete_keyboard(item_category="music", item_id=music_id)[0])
