import schedule
import time
from telegram import Bot
import config
import database.crud as crud
import help_funk as hf

import os


TOKEN = str(config.TOKEN)
GROUP_ID = str(config.GROUP_ID)

bot = Bot(token=str(TOKEN))


FILES_DIR = 'files'

def send_add_obj_yesterday_message():
    bot.send_message(GROUP_ID, f'Отчёт по добавленным объектам за {hf.get_yesterday()}')
    filename = f"объекты добавленные {hf.get_yesterday()}"

    data_db = crud.get_log_obj('2024-09-01', '2024-09-10')

    hf.create_excel_file(data_db, filename)

    bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename}.xls', 'rb'))



def send_add_obj_month_message():
    bot.send_message(GROUP_ID, 'Отчёт по добавленным объектам за месяц')

# schedule.every().day.at("08:00").do(send_morning_message)
# schedule.every().day.at("22:00").do(send_night_message)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

send_add_obj_yesterday_message()
