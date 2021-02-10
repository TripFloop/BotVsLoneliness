import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

iserotic_cb = CallbackData("iserotic", "bool_value")

yes_button = InlineKeyboardButton(text=emoji.emojize(":white_check_mark: Да"),callback_data=iserotic_cb.new(bool_value = True))
no_button = InlineKeyboardButton(text=emoji.emojize(":x: Нет"),callback_data=iserotic_cb.new(bool_value=False))
iserotic_markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[yes_button, no_button])
