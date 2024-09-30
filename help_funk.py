import pandas as pd 
from styleframe import StyleFrame

import os


FILES_DIR = 'files'


def get_yesterday():
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(days=1)
    return yesterday

def create_excel_file(data, file_name):
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
    sf.to_excel(excel_writer=excel_writer)
    excel_writer._save()
