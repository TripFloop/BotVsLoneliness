from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils import emoji
from filters import Leila, Sasha
from keyboards.inline.add_item_inline_keyboard import add_item_keyboard
from keyboards.inline.film_inline_keyboard import get_better_pages_keyboard_films, show_film
from keyboards.inline.item_delete_inline_keyboard import delete_keyboard
from keyboards.inline.text_inline_keyboard import pagination_call
from loader import dp, db


@dp.message_handler(Leila(), text=emoji.emojize(":film_frames: Списки наших любимых тайтлов и фильмов"))
@dp.message_handler(Sasha(), text=emoji.emojize(":film_frames: Списки наших любимых тайтлов и фильмов"))
async def show_text_menu_leila(message: types.Message):
    try:
        reply_markup = get_better_pages_keyboard_films(db.get_slice_of_films())
    except TypeError:
        await message.answer("Прости, но еще нет никаких тайтлов\nДобавь, плз :3",
                             reply_markup=add_item_keyboard(item_category="films")[0])
    await message.answer(text="""
                                Привет, вот наш список фильмов
                                """, reply_markup=reply_markup)


@dp.callback_query_handler(pagination_call.filter(key="films"))
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer()
    current_page = int(callback_data.get("page"))
    markup = get_better_pages_keyboard_films(db.get_slice_of_films(page=current_page), page=current_page)
    await call.message.edit_reply_markup(
        markup
    )


@dp.callback_query_handler(show_film.filter())
async def show_chosen_film(call: CallbackQuery, callback_data: dict):
    await call.answer()
    film_id = int(callback_data.get('film_id'))
    film_name, comment = db.get_film(film_id=film_id)
    await call.message.answer(text=f"{film_name}\n\n{comment}",
                              reply_markup=delete_keyboard(item_category='films', item_id=film_id)[0])
