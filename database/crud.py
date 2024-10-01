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
            models.Contragent.ca_name,
            models.MonitoringSystem.mon_sys_name,
            models.GlobalLogging.new_value,
                           ).outerjoin(
                models.Contragent, models.GlobalLogging.contragent_id == models.Contragent.ca_id
                ).outerjoin(
                        models.MonitoringSystem, models.GlobalLogging.sys_id == models.MonitoringSystem.mon_sys_id
                        ).filter(
                models.GlobalLogging.change_time.between(date_start, date_end),
                models.GlobalLogging.section_type=="object",
                models.GlobalLogging.action=="add",
            ).all()
    session.close()
    return result



