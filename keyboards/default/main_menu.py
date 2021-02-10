from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import emoji

menu_for_leila = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=emoji.emojize(":package: Послушай что он там наговорил :3"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":headphone: Меню голосовых сообщений"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":card_file_box: Меню твоих картинок"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":scroll: Меню текстов"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":film_frames: Списки наших любимых тайтлов и фильмов"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":multiple_musical_notes: Плейлист"))
    ],
    ], resize_keyboard=True
)

menu_for_me = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=emoji.emojize(":package: Послушай что она там наговорила"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":headphone: Меню голосовых сообщений"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":card_file_box: Меню твоих картинок"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":scroll: Меню текстов"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":film_frames: Списки наших любимых тайтлов и фильмов"))
    ],
    [
        KeyboardButton(text=emoji.emojize(":multiple_musical_notes: Плейлист"))
    ],
    ], resize_keyboard=True
)
