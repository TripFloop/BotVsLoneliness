from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import emoji

delete_cb = CallbackData("delete", "item_category", "owner", "item_id")


def delete_keyboard(item_category: str, owner: str, item_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=emoji.emojize(":wastebasket: Удалить"),
                                  callback_data=delete_cb.new(item_category=item_category, owner=owner,
                                                              item_id=item_id))
    markup.insert(button)
    return markup, button
