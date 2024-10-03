import schedule
import time
from telegram import Bot
import config
import database.crud as crud
import help_funk as hf

import os

from datetime import datetime, timedelta

TOKEN = str(config.TOKEN)
GROUP_ID = str(config.GROUP_ID)

bot = Bot(token=str(TOKEN))


FILES_DIR = 'files'

def send_add_obj_yesterday_message():
    yesterday = hf.get_yesterday()
    bot.send_message(GROUP_ID, f'Отчёт по добавленным объектам за {yesterday}')
    filename = f"объекты добавленные {yesterday}"

    clear_yea = datetime.now() - timedelta(days=1)
    data_db = crud.get_log_obj(
            f'{clear_yea.replace(hour=15, minute=0, second=0, microsecond=0)}',
            f'{datetime.now() + timedelta(days=1)}'
            )

    hf.create_excel_file(data_db, filename)

    bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename}.xls', 'rb'))



def send_add_obj_week_message():

    curent_date = datetime.now()
    current_week = None

    bot.send_message(GROUP_ID, 'Отчёт по добавленным объектам за неделю\n')

schedule.every().day.at("09:26").do(send_add_obj_yesterday_message)
#schedule.every().day.at("22:00").do(send_night_message)

while True:
    schedule.run_pending()
    time.sleep(1)

