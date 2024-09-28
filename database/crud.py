from os.path import join
import mysql_models as models
from bd_conectors import MysqlDatabase
from sqlalchemy import func


def get_log_obj(date_start, date_end):
    """
    Отдаёт логи по объектам за периуд времени
    """
    db = MysqlDatabase()
    session = db.session
    return session.query(models.LogChange).filter(
                models.LogChange.changes_date.between(date_start, date_end)
            )


