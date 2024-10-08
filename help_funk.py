import pandas as pd 
from styleframe import StyleFrame

import os


FILES_DIR = 'files'


def get_yesterday():
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(days=1)
    return yesterday

def create_excel_file(data, file_name):
    """ 
    Формирует EXCEL файл из данных БД
    """
    directory = FILES_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    df = pd.DataFrame(data, columns=[

        "Контрагент",
        "Система мониторинга",
        "Имя объекта"

        ])
    excel_writer = StyleFrame.ExcelWriter(f'{directory}/{file_name}.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Контрагент', 30)
    sf.set_column_width("Система мониторинга", 10)
    sf.set_column_width("Имя объекта", 30)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()

def week_report(data, file_name):
    """ 
    Формирует EXCEL отчёт по количеству добавленных и удалённых объектов из БД
    """

    directory = FILES_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['Система мониторинга', 'Добавленные', 'Удалённые']

    excel_writer = StyleFrame.ExcelWriter(f'{directory}/{file_name}.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Система мониторинга', 20)
    sf.set_column_width("Добавленные", 10)
    sf.set_column_width("Удалённые", 10)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()

