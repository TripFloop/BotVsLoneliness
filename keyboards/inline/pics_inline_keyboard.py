import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from .add_item_inline_keyboard import add_item_keyboard
from .item_delete_inline_keyboard import delete_keyboard
from .text_inline_keyboard import pagination_call


def get_page_keyboard_pics(owner: str, item_id: int, key="pics", page: int = 1, iserotic: bool = None):
    markup = InlineKeyboardMarkup(row_width=1)
    pages_buttons = list()
    first_page = 1
    first_page_text = "« 1"
    count_rows_in_db = db.count_number_of_rows_in_table("pics", owner=owner)
    count_rows_in_db = int(count_rows_in_db[0])
    max_pages = count_rows_in_db
    max_page_text = f"» {max_pages}"

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

    if next_page <= max_pages:
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
                                              page=max_pages)
        )
    )

    markup.row(*pages_buttons)
    print(item_id)
    if iserotic:
        markup.row(InlineKeyboardButton(text=emoji.emojize(":red_heart: Мяуротика :3"),
                                        callback_data=pagination_call.new(key=key, page="current_page")))
    markup.row(add_item_keyboard(item_category="pics", owner=owner))
    markup.row(delete_keyboard(item_category="pics", owner=owner, item_id=item_id)[1])
    return markup
