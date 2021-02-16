from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import Sasha, Leila
from keyboards.default import menu_for_me, menu_for_leila
from loader import dp


@dp.message_handler(CommandStart(), Sasha(), state="*")
async def bot_start(message: types.Message, state: FSMContext = None):
    await message.answer(text='Добро пожаловать в бота, который был создан со всей душой\n'
                              'Пожалуйста, используй команды', reply_markup=menu_for_me)
    if state:
        await state.finish()


@dp.message_handler(CommandStart(), Leila(), state="*")
async def bot_start(message: types.Message, state: FSMContext = None):
    await message.answer(text='Добро пожаловать в бота, который был создан со всей душой\n'
                              'Пожалуйста, используй команды', reply_markup=menu_for_leila)
    if state:
        await state.finish()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n'
                         'Если ты попал сюда случайно, то уходи\n'
                         'Этот бот не предназначен для мира живых')


@dp.message_handler(Sasha())
async def not_expected_text(message: types.Message):
    await message.answer('Используй кнопки')


@dp.message_handler(Leila())
async def not_expected_move(message: types.Message):
    await message.answer('Кись, что-то не так пошло')


@dp.message_handler()
async def get_out_message(message: types.Message):
    await message.answer('Проваливай отсюда, я как-то недоходчиво объяснил?')
