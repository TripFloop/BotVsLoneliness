from loader import scheduler
from scripts.time_script import scheduler_job
from utils.set_bot_commands import set_default_commands
import sqlite3


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)
    scheduler_job()
    try:
        db.create_tables()
    except sqlite3.OperationalError:
        pass


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
