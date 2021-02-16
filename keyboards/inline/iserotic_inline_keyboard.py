import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

iserotic_cb = CallbackData("iserotic", "bool_value")

def iserotic_keyboard():
    yes_button = InlineKeyboardButton(text=emoji.emojize(":white_check_mark: Да", True),
                                  callback_data=iserotic_cb.new(bool_value=True))
    no_button = InlineKeyboardButton(text=emoji.emojize(":x: Нет", True), callback_data=iserotic_cb.new(bool_value=False))
    iserotic_markup = InlineKeyboardMarkup(row_width=2)
    iserotic_markup.row(yes_button, no_button)
    return iserotic_markup

def iserotic_keyboard_leila():
    yes_button = InlineKeyboardButton(text=emoji.emojize(":wilted_flower: Эро", True),
                                  callback_data=iserotic_cb.new(bool_value=True))
    no_button = InlineKeyboardButton(text=emoji.emojize(":cherry_blossom: Милая", True), callback_data=iserotic_cb.new(bool_value=False))
    iserotic_markup = InlineKeyboardMarkup(row_width=2)
    iserotic_markup.row(yes_button, no_button)
    return iserotic_markup

