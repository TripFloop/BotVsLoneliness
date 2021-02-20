import logging
from loader import scheduler

from loader import db, bot
import random
from data.config import leila_id, owner_id
import datetime
from datetime import date


async def send_to_leila(iserotic: bool):
    try:
        try:
            caption = db.get_rand_text(iserotic=iserotic, owner="sasha")[0]
        except TypeError:
            caption = None
        await bot.send_photo(chat_id=leila_id, photo=db.get_rand_pic(iserotic=iserotic, owner="sasha")[0],
                             caption=caption)
    except Exception as err:
        logging.error(err)


async def send_to_sasha(iserotic: bool):
    try:
        try:
            caption = db.get_rand_text(iserotic=iserotic, owner="leila")[0]
        except TypeError:
            caption = None
        await bot.send_photo(chat_id=owner_id, photo=db.get_rand_pic(iserotic=iserotic, owner="leila")[0],
                             caption=caption)
    except Exception as err:
        logging.error(err)


def hours_for_pics_day():
    # Get 2 random hours for sending usual pics from 8 to 22 hours
    # Day time
    hours_for_sasha_day = random.randrange(8, 22)
    hours_for_leila_day = random.randrange(7, 21)
    return hours_for_sasha_day, hours_for_leila_day


def hours_for_pics_evening():
    # Get 2 random hours for sending evening pics from 23 to 3 hours
    # Evening time
    evening_hours = [0, 1, 2, 3, 23]
    evening_hours_for_leila = [hour - 1 if hour >= 1 else 23 for hour in evening_hours]
    hour_for_sasha_evening = random.choice(evening_hours)
    hour_for_leila_evening = random.choice(evening_hours_for_leila)
    return hour_for_sasha_evening, hour_for_leila_evening


def main_func():
    day_hours = random.randint(1, 3)
    leila_day_hours = [hours_for_pics_day()[1] for _ in range(1, day_hours + 1)]
    sasha_day_hours = [hours_for_pics_day()[0] for _ in range(1, day_hours + 1)]
    for hour in zip(sasha_day_hours, leila_day_hours):
        scheduler.add_job(send_to_sasha, "date", args=[False],
                          run_date=f"{date.today().year}-{date.today().month}-{date.today().day} {hour[0]}:00:05")
        scheduler.add_job(send_to_leila, "date", args=[False],
                          run_date=f"{date.today().year}-{date.today().month}-{date.today().day} {hour[1]}:00:05")
    eve_hour_sasha, eve_hour_leila = hours_for_pics_evening()
    scheduler.add_job(send_to_sasha,
                      "date",
                      args=[True],
                      run_date=f"{date.today().year}-{date.today().month}-{date.today().day} {eve_hour_sasha}:00:05")
    scheduler.add_job(send_to_leila,
                      "date",
                      args=[True],
                      run_date=f"{date.today().year}-{date.today().month}-{date.today().day} {eve_hour_leila}:00:05")
    logging.info("Today we have chosen such hours")
    logging.info(f"For Sasha - Day: {sasha_day_hours}, Night: {eve_hour_sasha}")
    logging.info(f"For Leila - Day: {leila_day_hours}, Night: {eve_hour_leila}")


def scheduler_job():
    scheduler.add_job(main_func, "cron", hour="0", minute="5")
