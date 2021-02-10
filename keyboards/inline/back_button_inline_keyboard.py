import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

func_cb = CallbackData("func", "prev_func")


def back_button_keyboard(prev_func: str):
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=emoji.emojize(":taxi: Назад"), callback_data=func_cb.new(prev_func=prev_func))
    markup.insert(button)
    return markup
