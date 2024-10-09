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
    """ 
    Добавленные объекты за предыдущий день
    """
    yesterday = hf.get_yesterday()
    filename = f"Объекты добавленные за {yesterday}"
    yesterday_with_fix_time = str(yesterday) + " 12:41:04"
    evening_time = datetime.now() + timedelta(days=1)

    data_db = crud.get_add_obj(
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


def send_add_dell_stop_obj_week_message():
    """ 
    Отчёт за предыдущую неделю
    по добавленным и удалённым и приостановленным
    """
    today = datetime.now()
    start_of_week = str(today - timedelta(days=today.weekday() + 7))
    file_name = f"Отчёт за неделю от {str(start_of_week).split(' ')[0]} до {str(today).split(' ')[0]}"

    week_data = crud.get_week_monitoring_data(start_of_week, today)

    if len(week_data) >= 1:

        hf.week_report(week_data, file_name)

        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{file_name}.xls', 'rb'))

        bot.send_message(GROUP_ID, f'{file_name}')
    else:
        pass


def send_monthly_report():
    """ 
    Отчёт за предыдущий месяц по добавленным и удалённым объектам
    """
    today = datetime.now()
    if today.day == 1:
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        filename = f"Отчёт за месяц с {first_day_of_last_month.date()} по {today.date()}"

        # Получаем данные за предыдущий месяц
        monthly_data = crud.get_week_monitoring_data(first_day_of_last_month, today)
        if len(monthly_data) >= 1:
            hf.week_report(monthly_data, filename)
            bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename}.xls', 'rb'))
            bot.send_message(GROUP_ID, f'{filename}')
        else:
            pass
    else:
        pass


schedule.every().day.at("09:26").do(send_add_obj_yesterday_message)
schedule.every().day.at("09:27").do(send_del_stop_obj_yesterday_message)
schedule.every().friday.at("09:30").do(send_add_dell_stop_obj_week_message)
schedule.every().day.at("09:40").do(send_monthly_report)

while True:
    schedule.run_pending()
    time.sleep(1)


