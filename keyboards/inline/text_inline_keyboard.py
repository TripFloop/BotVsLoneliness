import logging
from pprint import pprint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import emoji
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.add_item_inline_keyboard import add_item_keyboard
from loader import db

pagination_call = CallbackData("paginator", "key", "page")
show_text = CallbackData("show_text", "text_id")


def get_better_pages_keyboard(sliced_array, owner: str, page: int = 1):
    key = "text"
    markup = InlineKeyboardMarkup(row_width=1)
    MAX_ITEMS_PER_PAGE = 10
    texts_buttons = list()

    for text in sliced_array:
        id_in_buttons = sliced_array.index(text) + 1
        offset = (page - 1) * MAX_ITEMS_PER_PAGE
        id_in_buttons += offset
        if text[2]:
            iserotic_sign = emoji.emojize(":underage:")
        else:
            iserotic_sign = ""
        if len(text[1]) >= 20:
            text = list(text)
            text[1] = text[1][:20] + '...'
        texts_buttons.append(
            InlineKeyboardButton(
                text=f'{id_in_buttons}.  {text[1]} {iserotic_sign}',
                callback_data=show_text.new(text_id=text[0])
            )
        )

    pages_buttons = list()
    first_page = 1
    first_page_text = "« 1"

    count_rows_in_db = db.count_number_of_rows_in_table("texts_to_pic", owner=owner)
    count_rows_in_db = int(count_rows_in_db[0])

    if count_rows_in_db % MAX_ITEMS_PER_PAGE == 0:
        max_page = count_rows_in_db // MAX_ITEMS_PER_PAGE
    else:
        max_page = count_rows_in_db // MAX_ITEMS_PER_PAGE + 1

    max_page_text = f"» {max_page}"

    pages_buttons.append(
        InlineKeyboardButton(
            text=first_page_text,
            callback_data=pagination_call.new(key=key,
                                              page=first_page)
        )
    )

    previous_page = page - 1
    previous_page_text = f"< {previous_page}"

    if previous_page >= first_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=previous_page)
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(key=key,
                                                  page="current_page")
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=f"- {page} -",
            callback_data=pagination_call.new(key=key,
                                              page="current_page")
        )
    )

    next_page = page + 1
    next_page_text = f"{next_page} >"

    if next_page <= max_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=next_page)))
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(key=key,
                                                  page="current_page")
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=max_page_text,
            callback_data=pagination_call.new(key=key,
                                              page=max_page)
        )
    )
    for button in texts_buttons:
        markup.insert(button)

    markup.row(*pages_buttons)
    markup.row(add_item_keyboard(item_category='text', owner=owner)[1])
    return markup
