import schedule
import time
from telegram import Bot
import config
import database.crud as crud
import help_funk as hf


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
    yesterday_with_fix_time = str(yesterday) + " 15:41:04"
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
    yesterday_with_fix_time = str(yesterday) + " 15:41:04"
    evening_time = datetime.now() + timedelta(days=1)

    filename_count = f"Количество объектов на {datetime.now().date()}"

    all_obj = crud.get_count_all_obj()

    data_db = crud.get_del_stop_obj(
            f'{yesterday_with_fix_time}',
            f'{evening_time}'
            )

    if len(data_db) >= 1:

        hf.create_excel_file(data_db, filename)
        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename}.xls', 'rb'))
        bot.send_message(GROUP_ID, f'{filename}')

        hf.report_all_obj(all_obj, filename_count)
        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_count}.xls', 'rb'))
        bot.send_message(GROUP_ID, f'{filename_count}')
        time.sleep(1)

    else:
        pass


def send_add_dell_stop_obj_week_message():
    """ 
    Отчёт за предыдущую неделю
    по добавленным и удалённым и приостановленным
    """
    today = datetime.now()
    start_of_week = str(today - timedelta(days=today.weekday() + 7))


    filename_clear = f"Отчёт за неделю по местам с {start_of_week} по {today.date()}"
    filename_abon = f"Отчёт за неделю по абонентским местам с {start_of_week} по {today.date()}"
    filename_count = f"Количество объектов на {today.date()}"

    # Получаем данные за предыдущий месяц
    week_data_clear = crud.get_week_monitoring_data(start_of_week, today)
    week_data_abon = crud.get_week_monitoring_abon_data(start_of_week, today)
    all_obj = crud.get_count_all_obj()

    if len(week_data_clear) >= 1:
        hf.week_report(week_data_clear, filename_clear)
        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_clear}.xls', 'rb'))
        bot.send_message(GROUP_ID, f'{filename_clear}')
        time.sleep(1)

        hf.week_abon_report(week_data_abon, filename_abon)
        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_abon}.xls', 'rb'))
        bot.send_message(GROUP_ID, f'{filename_abon}')
        time.sleep(1)

        hf.report_all_obj(all_obj, filename_count)
        bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_count}.xls', 'rb'))
        bot.send_message(GROUP_ID, f'{filename_count}')
        time.sleep(1)

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

        filename_clear = f"Отчёт за месяц по местам с {first_day_of_last_month.date()} по {today.date()}"
        filename_abon = f"Отчёт за месяц по абонентским местам с {first_day_of_last_month.date()} по {today.date()}"

        filename_count = f"Количество объектов на {today.date()}"


        # Получаем данные за предыдущий месяц
        monthly_data_clear = crud.get_week_monitoring_data(first_day_of_last_month, today)
        monthly_data_abon = crud.get_week_monitoring_abon_data(first_day_of_last_month, today)
        all_obj = crud.get_count_all_obj()

        if len(monthly_data_clear) >= 1:
            hf.week_report(monthly_data_clear, filename_clear)
            bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_clear}.xls', 'rb'))
            bot.send_message(GROUP_ID, f'{filename_clear}')
            time.sleep(1)

            hf.week_abon_report(monthly_data_abon, filename_abon)
            bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_abon}.xls', 'rb'))
            bot.send_message(GROUP_ID, f'{filename_abon}')
            time.sleep(1)

            hf.report_all_obj(all_obj, filename_count)
            bot.send_document(GROUP_ID, open(f'{FILES_DIR}/{filename_count}.xls', 'rb'))
            bot.send_message(GROUP_ID, f'{filename_count}')
            time.sleep(1)


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


