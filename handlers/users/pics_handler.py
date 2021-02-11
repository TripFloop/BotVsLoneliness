import emoji
from aiogram import types
from aiogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup

from filters import Leila, Sasha
from keyboards.inline.add_item_inline_keyboard import add_item_keyboard
from keyboards.inline.pics_inline_keyboard import get_page_keyboard_pics
from keyboards.inline.text_inline_keyboard import pagination_call
from loader import dp, db
from utils.bool_conversation import int_to_bool


@dp.message_handler(Leila(), text=emoji.emojize(":card_file_box: Меню твоих картинок"))
async def show_pics_menu_leila(message: types.Message):
    owner = "leila"
    try:
        pic_id, file_id, iserotic = db.get_pic(owner=owner)
        iserotic = int_to_bool(iserotic)
        await message.answer_photo(photo=file_id,
                                   reply_markup=get_page_keyboard_pics(owner=owner, item_id=pic_id, iserotic=iserotic))
    except TypeError:
        await message.answer("В базе пока нет картинок, добавь первую",
                             reply_markup=InlineKeyboardMarkup(add_item_keyboard(item_category="pics", owner=owner),
                                                               row_width=1))


@dp.message_handler(Sasha(), text=emoji.emojize(":card_file_box: Меню твоих картинок"))
async def show_pics_menu_sasha(message: types.Message):
    owner = "sasha"
    try:
        pic_id, file_id, iserotic = db.get_pic(owner=owner)
        iserotic = int_to_bool(iserotic)
        await message.answer_photo(photo=file_id,
                                   reply_markup=get_page_keyboard_pics(owner=owner, item_id=pic_id, iserotic=iserotic))
    except TypeError:
        await message.answer("В базе пока нет картинок, добавь первую",
                             reply_markup=add_item_keyboard("pics", owner, 1)[0])




@dp.callback_query_handler(Leila(), pagination_call.filter(key="pics"))
async def show_chosen_pic(call: CallbackQuery, callback_data: dict):
    await call.answer()
    owner = "leila"
    current_page = int(callback_data.get("page"))
    pic_id, file_id, iserotic = db.get_pic(owner=owner, page=current_page)
    media = InputMediaPhoto(file_id)
    await call.message.edit_media(
        media=media,
        reply_markup=get_page_keyboard_pics(owner=owner, page=current_page, item_id=pic_id, iserotic=iserotic)
    )


@dp.callback_query_handler(Sasha(), pagination_call.filter(key="pics"))
async def show_chosen_pic(call: CallbackQuery, callback_data: dict):
    await call.answer()
    owner = "sasha"
    current_page = int(callback_data.get("page"))
    pic_id, file_id, iserotic = db.get_pic(owner=owner, page=current_page)
    media = InputMediaPhoto(file_id)
    await call.message.edit_media(
        media=media,
        reply_markup=get_page_keyboard_pics(owner=owner, page=current_page, item_id=pic_id, iserotic=iserotic)
    )

@dp.message_handler(commands=["test"])
async def test(message: types.Message):
    await message.answer("test", reply_markup=add_item_keyboard(item_category="pics", owner="sasha", row_width=1)[0])