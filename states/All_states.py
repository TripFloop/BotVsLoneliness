from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuStates(StatesGroup):
    add = State()
    add_pic = State()
    add_film = State()
    add_voice = State()
    add_text = State()
    add_music = State()
    voice_comment = State()
    iserotic_pic = State()
    add_mood = State()
    upload_music = State()
    iserotic_text = State()
    add_comment= State()