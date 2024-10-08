from os.path import join
import database.mysql_models as models
from database.bd_conectors import MysqlDatabase
from sqlalchemy import func, or_, and_


def get_add_obj(date_start, date_end):
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


def get_count_add_obj(date_start, date_end):
    """
    Отдаёт счётчик по объектам за период времени
    Добавленные
    """
    db = MysqlDatabase()
    session = db.session
    
    result = (
        session.query(
            models.MonitoringSystem.mon_sys_name,
            func.count(models.GlobalLogging.sys_id).label('count')
        )
        .join(
            models.GlobalLogging,
            models.GlobalLogging.sys_id == models.MonitoringSystem.mon_sys_id
        )
        .filter(
            models.GlobalLogging.change_time.between(date_start, date_end),
            models.GlobalLogging.section_type == "object",
            models.GlobalLogging.action == "add"
        )
        .group_by(models.MonitoringSystem.mon_sys_name)
        .all()
    )
    
    session.close()
    return result



def get_count_dell_stop_obj(date_start, date_end):
    """
    Отдаёт счётчик по объектам за период времени
    удалённые
    """
    db = MysqlDatabase()
    session = db.session
    
    result = (
        session.query(
            models.MonitoringSystem.mon_sys_name,
            func.count(models.GlobalLogging.sys_id).label('count')
        )
        .join(
            models.GlobalLogging,
            models.GlobalLogging.sys_id == models.MonitoringSystem.mon_sys_id
        )
        .filter(
            models.GlobalLogging.change_time.between(date_start, date_end),
                models.GlobalLogging.section_type=="object",
                or_(
                    models.GlobalLogging.action=="delete",
                    and_(
                        models.GlobalLogging.action == "update",
                        models.GlobalLogging.new_value.like("%_приост%"),
                    )
                )

        )
        .group_by(models.MonitoringSystem.mon_sys_name)
        .all()
    )
    
    session.close()
    return result


def get_week_monitoring_data(date_start, date_end):
    added_data = get_count_add_obj(date_start, date_end)
    deleted_data = get_count_dell_stop_obj(date_start, date_end)

    monitoring_dict = {}

    # Заполнение словаря добавленными данными
    for mon_sys_name, count in added_data:
        monitoring_dict[mon_sys_name] = {'added': count, 'deleted': 0}

    # Заполнение словаря удалёнными данными
    for mon_sys_name, count in deleted_data:
        if mon_sys_name in monitoring_dict:
            monitoring_dict[mon_sys_name]['deleted'] = count
        else:
            monitoring_dict[mon_sys_name] = {'added': 0, 'deleted': count}

    return monitoring_dict

