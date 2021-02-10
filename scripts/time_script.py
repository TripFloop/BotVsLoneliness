import logging
import schedule
from loader import scheduler

from loader import db, bot
import random
from data.config import Leila_id, owner_id


async def send_to_Leila(iserotic: bool):
    try:
        await bot.send_photo(chat_id=Leila_id, photo=db.get_rand_pic(iserotic=iserotic, from_name='Sasha'),
                             caption=db.get_rand_text(iserotic=iserotic))
    except Exception as err:
        logging.error(err)
    return schedule.CancelJob


async def send_to_Sasha(iserotic: bool):
    try:
        await bot.send_photo(chat_id=owner_id, photo=db.get_rand_pic(iserotic=iserotic, from_name='Leila'),
                             caption=db.get_rand_text(iserotic=iserotic))
    except Exception as err:
        logging.error(err)
    return schedule.CancelJob


def hours_for_pics_day():
    # Get 2 random hours for sending usual pics from 8 to 22 hours
    # Day time
    hours_for_sasha_day = random.randrange(8, 22)
    hours_for_leila_day = random.randrange(8, 22)
    return hours_for_sasha_day, hours_for_leila_day


def hours_for_pics_evening():
    # Get 2 random hours for sending evening pics from 23 to 3 hours
    # Evening time
    evening_hours = [0, 1, 2, 3, 23]
    hour_for_sasha_evening = random.choice(evening_hours)
    hour_for_leila_evening = random.choice(evening_hours)
    return hour_for_sasha_evening, hour_for_leila_evening


def make_all_hours_in_one_place():
    times_per_day = random.randint(1, 3)
    hours_day_leila_dict = {}
    hours_day_sasha_dict = {}
    for time in range(times_per_day):
        hour_for_sasha, hour_for_leila = hours_for_pics_day()
        hours_day_sasha_dict.update({hour_for_sasha: time})
        hours_day_leila_dict.update({hour_for_leila: time})
    evening_hour_for_sasha, evening_hour_for_Leila = hours_for_pics_evening()
    logging.info('Im here')
    return hours_day_sasha_dict, hours_day_leila_dict, evening_hour_for_sasha, evening_hour_for_Leila


def main_script(hours_day_sasha_dict: dict, hours_day_leila_dict: dict, evening_hour_for_sasha: int,
                evening_hour_for_leila: int):
    for hour in hours_day_sasha_dict:
        scheduler.add_job(send_to_Sasha(iserotic=False), trigger="cron", hour=hour,
                          id=f'day_sasha_{hours_day_sasha_dict[hour]}')
    for hour in hours_day_leila_dict:
        scheduler.add_job(send_to_Leila(iserotic=False), trigger="cron", hour=hour,
                          id=f'day_leila_{hours_day_leila_dict[hour]}')
    # --------------------Night time---------------------------
    scheduler.add_job(send_to_Sasha(iserotic=True), trigger="cron", hour=evening_hour_for_sasha, id='evening_sasha')
    scheduler.add_job(send_to_Leila(iserotic=True), trigger="cron", hour=evening_hour_for_leila, id='evening_leila')

logging.info(callable(make_all_hours_in_one_place()))


scheduler.add_job(func=make_all_hours_in_one_place, trigger="cron", hour=23, minute=57)
#scheduler.add_job(clear_pics_jobs, trigger="cron", hour=23, minute=58)
#scheduler.add_job(main_script(), trigger="cron", hour=23, minute=59)
