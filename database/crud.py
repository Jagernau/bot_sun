from os.path import join
import database.mysql_models as models
from database.bd_conectors import MysqlDatabase
from sqlalchemy import func


def get_log_obj(date_start, date_end):
    """
    Отдаёт логи по объектам за периуд времени
    """
    db = MysqlDatabase()
    session = db.session
    result = session.query(
            models.GlobalLogging.old_value, 
            models.GlobalLogging.new_value
                           ).filter(
                models.GlobalLogging.change_time.between(date_start, date_end)
            ).all()
    session.close()
    return result



