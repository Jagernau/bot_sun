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
    df.columns = ['Система мониторинга', 'Занялось мест', 'Освободилось мест']
    df['ДИНАМИКА ПО МЕСТАМ'] = df['Занялось мест'] - df['Освободилось мест']
    total_dynamic = df['ДИНАМИКА ПО МЕСТАМ'].sum()
    total_row = pd.DataFrame({
        'Система мониторинга': ['Итого'],
        'Занялось мест': [df['Занялось мест'].sum()],
        'Освободилось мест': [df['Освободилось мест'].sum()],
        'ДИНАМИКА ПО МЕСТАМ': [total_dynamic]
    })
    df = pd.concat([df, total_row], ignore_index=True)



    excel_writer = StyleFrame.ExcelWriter(f'{directory}/{file_name}.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Система мониторинга', 20)
    sf.set_column_width("Занялось мест", 18)
    sf.set_column_width("Освободилось мест", 20)
    sf.set_column_width("ДИНАМИКА ПО МЕСТАМ", 15)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()



def week_abon_report(data, file_name):
    """ 
    Формирует EXCEL отчёт по количеству добавленных и удалённых объектов из БД
    На абонентке
    """

    directory = FILES_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['Система мониторинга', 'Встало на абонентку', 'Ушло с абонентки']
    df['ДИНАМИКА ПО АБОН'] = df['Встало на абонентку'] - df['Ушло с абонентки']
    total_dynamic = df['ДИНАМИКА ПО АБОН'].sum()
    total_row = pd.DataFrame({
        'Система мониторинга': ['Итого'],
        'Встало на абонентку': [df['Встало на абонентку'].sum()],
        'Ушло с абонентки': [df['Ушло с абонентки'].sum()],
        'ДИНАМИКА ПО АБОН': [total_dynamic]
    })
    df = pd.concat([df, total_row], ignore_index=True)



    excel_writer = StyleFrame.ExcelWriter(f'{directory}/{file_name}.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Система мониторинга', 20)
    sf.set_column_width("Встало на абонентку", 18)
    sf.set_column_width("Ушло с абонентки", 20)
    sf.set_column_width("ДИНАМИКА ПО АБОН", 15)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()



def report_all_obj(data, file_name):
    """ 
    Формирует EXCEL файл из данных БД
    """
    directory = FILES_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    df = pd.DataFrame(data, columns=[

        "Система мониторинга",
        "Количество объектов"

        ])

    total_row = pd.DataFrame({
        'Система мониторинга': ['Итого'],
        "Количество объектов": [df["Количество объектов"].sum()],
    })
    df = pd.concat([df, total_row], ignore_index=True)

    excel_writer = StyleFrame.ExcelWriter(f'{directory}/{file_name}.xls')
    sf = StyleFrame(df)
    sf.set_column_width("Система мониторинга", 30)
    sf.set_column_width("Количество объектов", 30)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()

