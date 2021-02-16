import logging
import emoji
from aiogram import types
from aiogram.types import CallbackQuery

from filters import Leila, Sasha
from keyboards.inline.item_delete_inline_keyboard import delete_cb, delete_keyboard
from keyboards.inline.text_inline_keyboard import get_better_pages_keyboard, pagination_call, show_text
from loader import dp, db, bot


@dp.message_handler(Leila(), text=emoji.emojize(":scroll: Меню текстов"))
async def show_text_menu_leila(message: types.Message):
    await message.answer(text="""
                                Привет, вот твой список текстов, выбирай, что нужно
                                """, reply_markup=get_better_pages_keyboard(db.get_slice_of_texts(owner='leila'),
                                                                            owner='leila'))


@dp.message_handler(Sasha(), text=emoji.emojize(":scroll: Меню текстов"))
async def show_text_menu_sasha(message: types.Message):
    await message.answer(text="""
                                Привет, вот твой список текстов, выбирай, что нужно
                                """, reply_markup=get_better_pages_keyboard(db.get_slice_of_texts(owner='sasha'),
                                                                            owner='sasha'))


@dp.callback_query_handler(pagination_call.filter(page="current_page"))
async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


@dp.callback_query_handler(Leila(), pagination_call.filter(key="text"))
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer()
    current_page = int(callback_data.get("page"))
    markup = get_better_pages_keyboard(db.get_slice_of_texts(owner='leila', page=current_page), page=current_page,
                                       owner='leila')
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(Sasha(), pagination_call.filter(key="text"))
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer()
    current_page = int(callback_data.get("page"))
    markup = get_better_pages_keyboard(db.get_slice_of_texts(owner='sasha', page=current_page), page=current_page,
                                       owner='sasha')
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(Leila(), show_text.filter())
async def show_text_for_leila(call: CallbackQuery, callback_data: dict):
    await call.answer()
    text_id = int(callback_data.get('text_id'))
    text = str(db.get_text(owner='leila', text_id=text_id))
    await bot.send_message(text=text, chat_id=call.message.chat.id,
                           reply_markup=delete_keyboard(item_category='text', owner='leila', item_id=text_id)[0])


@dp.callback_query_handler(Sasha(), show_text.filter())
async def show_text_for_sasha(call: CallbackQuery, callback_data: dict):
    await call.answer()
    text_id = int(callback_data.get('text_id'))
    text = str(db.get_text(owner='sasha', text_id=text_id))
    await bot.send_message(text=text, chat_id=call.message.chat.id,
                           reply_markup=delete_keyboard(item_category='text', owner='sasha', item_id=text_id)[0])


@dp.callback_query_handler(delete_cb.filter())
async def delete_item(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get("item_id")
    owner = callback_data.get("owner")
    item_category = callback_data.get("item_category")
    if item_category == "voice_messages":
        db.delete_voice_message(voice_message_id=item_id, owner=owner)
    elif item_category == "text":  # complete
        db.delete_text(text_id=item_id, owner=owner)
        if owner == "leila":
            await bot.send_message(chat_id=call.message.chat.id, text="""
                                         Привет, вот твой список текстов, выбирай, что нужно
                                         """, reply_markup=get_better_pages_keyboard(db.get_all_text(owner='leila'),
                                                                                     owner='leila'))
        elif owner == "sasha":
            await bot.send_message(chat_id=call.message.chat.id, text="""
                                         Привет, вот твой список текстов, выбирай, что нужно
                                         """, reply_markup=get_better_pages_keyboard(db.get_all_text(owner='sasha'),
                                                                                     owner='sasha'))
    elif item_category == "films":
        db.delete_film(film_id=item_id)
    elif item_category == "music":
        db.delete_music(music_id=item_id)
    elif item_category == "pics":  # complete
        db.delete_pic(pic_id=item_id)
    await call.answer(text=f"Вы успешно удалили {item_category}")
    if item_category != "pics":
        await call.message.delete()
