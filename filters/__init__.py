from aiogram import Dispatcher

from .lovers_filter import Sasha, Leila


def setup(dp: Dispatcher):
    dp.filters_factory.bind(Sasha)
    dp.filters_factory.bind(Leila)
    pass
