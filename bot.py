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
    filename = f"Объекты добавленные за {yesterday}"
    yesterday_with_fix_time = str(yesterday) + " 12:41:04"
    evening_time = datetime.now() + timedelta(days=1)

    data_db = crud.get_log_obj(
            f'{yesterday_with_fix_time}',
            f'{evening_time}'
            )
    if len(data_db) >= 1:
        hf.create_excel_file(data_db, filename)

        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename}.xls', 'rb'))

        bot.send_message(GROUP_ID, f'{filename}')
    else:
        pass


def send_del_stop_obj_yesterday_message():
    """ 
    отправляет таблицу с удалёнными и приостановлеными объектами в excel
    """
    yesterday = hf.get_yesterday()
    filename = f"Объекты удалённые и приостановленные за {yesterday}"
    yesterday_with_fix_time = str(yesterday) + " 12:41:04"
    evening_time = datetime.now() + timedelta(days=1)

    data_db = crud.get_del_stop_obj(
            f'{yesterday_with_fix_time}',
            f'{evening_time}'
            )

    if len(data_db) >= 1:

        hf.create_excel_file(data_db, filename)

        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename}.xls', 'rb'))

        bot.send_message(GROUP_ID, f'{filename}')
    else:
        pass


def send_add_obj_week_message():

    curent_date = datetime.now()
    current_week = None

    bot.send_message(GROUP_ID, 'Отчёт по добавленным объектам за неделю\n')


schedule.every().day.at("09:26").do(send_add_obj_yesterday_message)
schedule.every().day.at("09:27").do(send_del_stop_obj_yesterday_message)

# send_add_obj_yesterday_message()
# send_del_stop_obj_yesterday_message()

while True:
    schedule.run_pending()
    time.sleep(1)

