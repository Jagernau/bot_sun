from os.path import join
import database.mysql_models as models
from database.bd_conectors import MysqlDatabase
from sqlalchemy import func, or_, and_
from sqlalchemy import case

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
            case(
                [
                    (models.GlobalLogging.new_value == '0', models.GlobalLogging.old_value)
                ],
                else_=models.GlobalLogging.new_value
                ).label("value")
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


def get_count_add_abonet_obj(date_start, date_end):
    """
    Отдаёт счётчик по объектам за период времени
    Добавленные на абонентке
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
            models.GlobalLogging.section_type == "object")
        .filter(
            or_(
                and_(
                    models.GlobalLogging.action == "add",
                    func.lower(models.GlobalLogging.new_value).notlike("%приост%"),
                    func.lower(models.GlobalLogging.new_value).notlike("%тест%"),
                    func.lower(models.GlobalLogging.new_value).notlike("%новт%"),
                    func.lower(models.GlobalLogging.new_value).notlike("%ппро%"),
                    func.lower(models.GlobalLogging.new_value).notlike("%пере%"),
                ),
                and_(
                    models.GlobalLogging.action == "update",
                    models.GlobalLogging.field == "object_status_id",
                    models.GlobalLogging.new_value == "3",
                    models.GlobalLogging.old_value != "3"
                )
            )
        )
        .group_by(models.MonitoringSystem.mon_sys_name)
        .all()
    )
    
    session.close()
    return result



def get_count_dell_stop_obj(date_start, date_end):
    """
    Отдаёт счётчик по объектам за период времени
    удалённые места
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
                models.GlobalLogging.action=="delete",
        )
        .group_by(models.MonitoringSystem.mon_sys_name)
        .all()
    )
    
    session.close()
    return result


def get_count_dell_stop_abonent_obj(date_start, date_end):
    """
    Отдаёт счётчик по объектам за период времени
    удалённые с абонентки
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
            models.GlobalLogging.section_type=="object")
        .filter(
            or_(

                and_(
                    models.GlobalLogging.action=="delete",
                    func.lower(models.GlobalLogging.old_value).notlike("%приост%"),
                    func.lower(models.GlobalLogging.old_value).notlike("%тест%"),
                    func.lower(models.GlobalLogging.old_value).notlike("%новт%"),
                    func.lower(models.GlobalLogging.old_value).notlike("%ппро%"),
                    func.lower(models.GlobalLogging.old_value).notlike("%пере%"),

                ),
                and_(
                    models.GlobalLogging.action == "update",
                    models.GlobalLogging.field == "object_status_id",
                    models.GlobalLogging.new_value != "3",
                    models.GlobalLogging.old_value == "3",
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




def get_week_monitoring_abon_data(date_start, date_end):
    added_data_abon = get_count_add_abonet_obj(date_start, date_end)
    deleted_data_abon = get_count_dell_stop_abonent_obj(date_start, date_end)

    monitoring_dict = {}

    # Заполнение словаря добавленными данными
    for mon_sys_name, count in added_data_abon:
        monitoring_dict[mon_sys_name] = {'added': count, 'deleted': 0}

    # Заполнение словаря удалёнными данными
    for mon_sys_name, count in deleted_data_abon:
        if mon_sys_name in monitoring_dict:
            monitoring_dict[mon_sys_name]['deleted'] = count
        else:
            monitoring_dict[mon_sys_name] = {'added': 0, 'deleted': count}


    return monitoring_dict


def get_count_all_obj():
    """
    Отдаёт счётчик по количествам объектов
    """
    db = MysqlDatabase()
    session = db.session
    
    result = (
        session.query(
            models.MonitoringSystem.mon_sys_name,
            func.count(models.CaObject.sys_mon_id).label('count')
        )
        .join(
            models.CaObject,
            models.CaObject.sys_mon_id == models.MonitoringSystem.mon_sys_id
        )
        .filter(
            models.CaObject.object_status != 7)
        .group_by(models.MonitoringSystem.mon_sys_name)
        .all()
    )
    
    session.close()
    return result

