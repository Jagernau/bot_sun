from os.path import join
import database.mysql_models as models
from database.bd_conectors import MysqlDatabase
from sqlalchemy import func, or_, and_


def get_log_obj(date_start, date_end):
    """
    Отдаёт логи по объектам за периуд времени
    Добавленные
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



def get_del_stop_obj(date_start, date_end):
    """
    Отдаёт логи по объектам за периуд времени
    Удалённые и деактивированные.
    """
    db = MysqlDatabase()
    session = db.session
    result = session.query(
            models.Contragent.ca_name,
            models.MonitoringSystem.mon_sys_name,
            models.GlobalLogging.old_value,
                           ).outerjoin(
                models.Contragent, models.GlobalLogging.contragent_id == models.Contragent.ca_id
                ).outerjoin(
                        models.MonitoringSystem, models.GlobalLogging.sys_id == models.MonitoringSystem.mon_sys_id
                        ).filter(
                models.GlobalLogging.change_time.between(date_start, date_end),
                models.GlobalLogging.section_type=="object",
                or_(
                    models.GlobalLogging.action=="delete",
                    and_(
                        models.GlobalLogging.action == "update",
                        models.GlobalLogging.new_value.like("%_приост%"),
                    )
                )
            ).all()
    session.close()
    return result
