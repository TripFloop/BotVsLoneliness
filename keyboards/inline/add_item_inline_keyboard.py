from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import emoji
from aiogram.utils.callback_data import CallbackData

add_cb = CallbackData("add_item", "item_category", "owner")


def add_item_keyboard(item_category: str, owner: str, row_width = 3):
    text = emoji.emojize(text=":thought_balloon: Добавить")
    if item_category == "voice_message":
        text = emoji.emojize(text=":studio_microphone: Запись")
    button = InlineKeyboardButton(text=text,
                                  callback_data=add_cb.new(
                                      item_category=item_category, owner=owner))
    reply_markup = InlineKeyboardMarkup(row_width)
    reply_markup.insert(button)
    return reply_markup, button
