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
    df.columns = ['Система мониторинга', 'Добавленные', 'Удалённые и блокированные']
    df['ДИНАМИКА'] = df['Добавленные'] - df['Удалённые и блокированные']
    total_dynamic = df['ДИНАМИКА'].sum()
    total_row = pd.DataFrame({
        'Система мониторинга': ['Итого'],
        'Добавленные': [df['Добавленные'].sum()],
        'Удалённые и блокированные': [df['Удалённые и блокированные'].sum()],
        'ДИНАМИКА': [total_dynamic]
    })
    df = pd.concat([df, total_row], ignore_index=True)



    excel_writer = StyleFrame.ExcelWriter(f'{directory}/{file_name}.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Система мониторинга', 20)
    sf.set_column_width("Добавленные", 18)
    sf.set_column_width("Удалённые и блокированные", 20)
    sf.set_column_width("ДИНАМИКА", 15)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()

