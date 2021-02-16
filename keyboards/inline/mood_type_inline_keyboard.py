import emoji
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

mood_cb = CallbackData("mood", "mood_type")


def mood_inline():
    button_happy = InlineKeyboardButton(text=emoji.emojize(":sunny: Happy and exciting", True),
                                        callback_data=mood_cb.new(mood_type="happy"))
    button_calm = InlineKeyboardButton(text=emoji.emojize(":ear_of_rice: Calm and sad", True),
                                       callback_data=mood_cb.new(mood_type="sad"))
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(button_happy)
    markup.row(button_calm)
    return markup
