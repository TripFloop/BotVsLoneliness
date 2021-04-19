from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from utils.db_api.db import Database
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
# Didn't used Redis storage, need to refactor
dp = Dispatcher(bot, storage=storage)
db = Database()
scheduler = AsyncIOScheduler()
