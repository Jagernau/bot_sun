from sqlalchemy import BigInteger, CheckConstraint, Column, Date, DateTime, ForeignKey, Index, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class CellOperator(Base):
    __tablename__ = 'Cell_operator'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(60), nullable=False, comment='Имя сотового оператора')
    ca_price = Column(Integer, comment='цена для клиентов')
    sun_price = Column(Integer, comment='Цена для Сантел')

    sim_cards = relationship('SimCards', back_populates='Cell_operator')


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150, 'utf8mb3_unicode_ci'), nullable=False, unique=True)

    auth_user_groups = relationship('AuthUserGroups', back_populates='group')
    auth_group_permissions = relationship('AuthGroupPermissions', back_populates='group')


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String(128, 'utf8mb3_unicode_ci'), nullable=False)
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150, 'utf8mb3_unicode_ci'), nullable=False, unique=True)
    first_name = Column(String(150, 'utf8mb3_unicode_ci'), nullable=False)
    last_name = Column(String(150, 'utf8mb3_unicode_ci'), nullable=False)
    email = Column(String(254, 'utf8mb3_unicode_ci'), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)
    last_login = Column(DATETIME(fsp=6))

    auth_user_groups = relationship('AuthUserGroups', back_populates='user')
    devices_logger_commands = relationship('DevicesLoggerCommands', back_populates='auth_user')
    django_admin_log = relationship('DjangoAdminLog', back_populates='user')
    auth_user_user_permissions = relationship('AuthUserUserPermissions', back_populates='user')
    devices = relationship('Devices', back_populates='itprogrammer')
    sim_cards = relationship('SimCards', back_populates='itprogrammer')


class DevicesVendor(Base):
    __tablename__ = 'devices_vendor'

    id = Column(Integer, primary_key=True)
    vendor_name = Column(String(35, 'utf8mb3_unicode_ci'))

    devices_brands = relationship('DevicesBrands', back_populates='devices_vendor')


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    app_label = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)
    model = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)

    auth_permission = relationship('AuthPermission', back_populates='content_type')
    django_admin_log = relationship('DjangoAdminLog', back_populates='content_type')


class DjangoMigrations(Base):
    __tablename__ = 'django_migrations'

    id = Column(BigInteger, primary_key=True)
    app = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40, 'utf8mb3_unicode_ci'), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


class GlobalLogging(Base):
    __tablename__ = 'global_logging'

    id = Column(Integer, primary_key=True)
    section_type = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)
    edit_id = Column(Integer, nullable=False)
    field = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)
    old_value = Column(String(255, 'utf8mb3_unicode_ci'))
    new_value = Column(String(255, 'utf8mb3_unicode_ci'))
    change_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    sys_id = Column(Integer, comment='Система мониторинга')
    action = Column(String(100, 'utf8mb3_unicode_ci'))


class GuaranteeTerms(Base):
    __tablename__ = 'guarantee_terms'

    gt_id = Column(Integer, primary_key=True, comment='ID гарантийного срока')
    gt_term = Column(Integer, comment='Срок гарантии (дней)')
    gt_type = Column(VARCHAR(255), comment='Тип гарантии')


class Holdings(Base):
    __tablename__ = 'holdings'

    holding_id = Column(Integer, primary_key=True)
    holding_name = Column(String(255, 'utf8mb3_unicode_ci'))

    Contragents = relationship('Contragents', back_populates='ca_holding')


class MonitoringSystem(Base):
    __tablename__ = 'monitoring_system'

    mon_sys_id = Column(Integer, primary_key=True)
    mon_sys_name = Column(VARCHAR(60), comment='Название системы мониторинга')
    mon_sys_obj_price_suntel = Column(Integer, comment='Стоимость объекта для Сантел')
    mon_sys_ca_obj_price_default = Column(Integer, comment='Базовая стоимость объекта для Контрагента')

    Login_users = relationship('LoginUsers', back_populates='system')
    ca_objects = relationship('CaObjects', back_populates='sys_mon')
    clients_in_system_monitor = relationship('ClientsInSystemMonitor', back_populates='system_monitor')
    devices = relationship('Devices', back_populates='sys_mon')


class ObjectStatuses(Base):
    __tablename__ = 'object_statuses'

    status_id = Column(Integer, primary_key=True)
    abon_bool = Column(TINYINT(1), nullable=False, comment='На абонентке или нет')
    status = Column(VARCHAR(50))

    ca_objects = relationship('CaObjects', back_populates='object_statuses')


t_Одинаковые_imei_терминалов = Table(
    'Одинаковые imei терминалов', metadata,
    Column('device_imei', String(60)),
    Column('count', BigInteger, server_default=text("'0'"))
)


t_Одинаковые_инн = Table(
    'Одинаковые инн', metadata,
    Column('ca_inn', String(60)),
    Column('count', BigInteger, server_default=text("'0'"))
)


t_Одинаковые_логины = Table(
    'Одинаковые логины', metadata,
    Column('login', String(60)),
    Column('count', BigInteger, server_default=text("'0'"))
)


class Contragents(Base):
    __tablename__ = 'Contragents'

    ca_id = Column(Integer, primary_key=True)
    ca_holding_id = Column(ForeignKey('holdings.holding_id'), index=True, comment='ID холдинга')
    ca_name = Column(VARCHAR(255), comment='Название контрагента')
    ca_shortname = Column(String(250, 'utf8mb3_unicode_ci'))
    ca_inn = Column(VARCHAR(60), comment='ИНН контрагента')
    ca_kpp = Column(VARCHAR(60), comment='КПП контрагента')
    ca_bill_account_num = Column(VARCHAR(60), comment='Расчетный счет')
    ca_bill_account_bank_name = Column(VARCHAR(60), comment='Наименование банка')
    ca_bill_account_ogrn = Column(VARCHAR(60), comment='ОГРН')
    ca_edo_connect = Column(TINYINT(1), comment='Обмен ЭДО')
    ca_field_of_activity = Column(VARCHAR(260), comment='Сфера деятельности')
    ca_type = Column(VARCHAR(60), comment='тип компании')
    unique_onec_id = Column(VARCHAR(100), comment='уникальный id в 1С контрагента ')
    registration_date = Column(Date, comment='Дата регистрации в 1С')
    key_manager = Column(VARCHAR(200), comment='Основной менеджер ')
    actual_address = Column(VARCHAR(300), comment='Фактический адрес ')
    registered_office = Column(VARCHAR(300), comment='Юридический адрес ')
    phone = Column(VARCHAR(200), comment='Телефон ')

    ca_holding = relationship('Holdings', back_populates='Contragents')
    Login_users = relationship('LoginUsers', back_populates='contragent')
    ca_contacts = relationship('CaContacts', back_populates='ca')
    ca_contracts = relationship('CaContracts', back_populates='ca')
    ca_objects = relationship('CaObjects', back_populates='contragent')
    clients_in_system_monitor = relationship('ClientsInSystemMonitor', back_populates='client')
    devices = relationship('Devices', back_populates='contragent')
    object_vehicles = relationship('ObjectVehicles', back_populates='vehicle_ca')
    sim_cards = relationship('SimCards', back_populates='contragent')


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False)
    codename = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)

    content_type = relationship('DjangoContentType', back_populates='auth_permission')
    auth_group_permissions = relationship('AuthGroupPermissions', back_populates='permission')
    auth_user_user_permissions = relationship('AuthUserUserPermissions', back_populates='permission')


class AuthUserGroups(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup', back_populates='auth_user_groups')
    user = relationship('AuthUser', back_populates='auth_user_groups')


class DevicesBrands(Base):
    __tablename__ = 'devices_brands'

    id = Column(Integer, primary_key=True)
    name = Column(String(200, 'utf8mb3_unicode_ci'))
    devices_vendor_id = Column(ForeignKey('devices_vendor.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Id Вендора терминалов')

    devices_vendor = relationship('DevicesVendor', back_populates='devices_brands')
    devices = relationship('Devices', back_populates='devices_brand')
    devices_commands = relationship('DevicesCommands', back_populates='devices_brands')


class DevicesLoggerCommands(Base):
    __tablename__ = 'devices_logger_commands'
    __table_args__ = {'comment': 'Таблица логгов команд'}

    id = Column(Integer, primary_key=True)
    command_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='Время отправки команды ')
    command_resresponse = Column(VARCHAR(200), nullable=False, comment='Ответ на команду')
    command_send = Column(VARCHAR(200), nullable=False, comment='Команда')
    programmer = Column(ForeignKey('auth_user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='Кто отправил команду')
    terminal_imei = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False, comment='imei терминала')

    auth_user = relationship('AuthUser', back_populates='devices_logger_commands')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('(`action_flag` >= 0)'),
    )

    id = Column(Integer, primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_repr = Column(String(200, 'utf8mb3_unicode_ci'), nullable=False)
    action_flag = Column(SMALLINT, nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)
    object_id = Column(LONGTEXT)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)

    content_type = relationship('DjangoContentType', back_populates='django_admin_log')
    user = relationship('AuthUser', back_populates='django_admin_log')


class LoginUsers(Base):
    __tablename__ = 'Login_users'

    id = Column(Integer, primary_key=True)
    account_status = Column(TINYINT, nullable=False, server_default=text("'1'"), comment='Состояние учётки 0-остановлена, 1-не подтверждена но активна, 2-подтверждена и активна')
    client_name = Column(VARCHAR(200))
    login = Column(VARCHAR(60))
    email = Column(VARCHAR(60))
    password = Column(VARCHAR(60))
    date_create = Column(Date)
    system_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    contragent_id = Column(ForeignKey('Contragents.ca_id', ondelete='SET NULL', onupdate='RESTRICT'), index=True, comment='ID контрагента')
    comment_field = Column(String(270, 'utf8mb3_unicode_ci'), comment='Поле с комментариями')
    ca_uid = Column(VARCHAR(100), comment='Уникальный id контрагента')

    contragent = relationship('Contragents', back_populates='Login_users')
    system = relationship('MonitoringSystem', back_populates='Login_users')


class AuthGroupPermissions(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup', back_populates='auth_group_permissions')
    permission = relationship('AuthPermission', back_populates='auth_group_permissions')


class AuthUserUserPermissions(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission', back_populates='auth_user_user_permissions')
    user = relationship('AuthUser', back_populates='auth_user_user_permissions')


class CaContacts(Base):
    __tablename__ = 'ca_contacts'

    ca_contact_id = Column(Integer, primary_key=True)
    ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='id компании')
    ca_contact_name = Column(VARCHAR(255), comment='Имя контактного лица')
    ca_contact_surname = Column(VARCHAR(255), comment='Фамилия контактного лица')
    ca_contact_middlename = Column(VARCHAR(255), comment='Отчество контактного лица')
    ca_contact_cell_num = Column(VARCHAR(255), unique=True, comment='Сотовый телефон контакт. лица')
    ca_contact_work_num = Column(VARCHAR(255), comment='Рабочий телефон к.л.')
    ca_contact_email = Column(VARCHAR(255), comment='Электр.почт. к.л')
    ca_contact_position = Column(VARCHAR(255), comment='Должность к.л.')

    ca = relationship('Contragents', back_populates='ca_contacts')


class CaContracts(Base):
    __tablename__ = 'ca_contracts'

    contract_id = Column(Integer, primary_key=True)
    ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='ID контрагента')
    contract_type = Column(VARCHAR(50), comment='Тип договора')
    contract_num_prefix = Column(VARCHAR(50), comment='Префикс номера договора')
    contract_num = Column(VARCHAR(50), comment='Номер договора')
    contract_payment_term = Column(VARCHAR(50), comment='условия оплаты')
    contract_payment_period = Column(VARCHAR(50), comment='Период оплаты')
    contract_start_date = Column(Date, comment='Дата заключения договора')
    contract_expired_date = Column(Date, comment='Дата завершения договора')

    ca = relationship('Contragents', back_populates='ca_contracts')


class CaObjects(Base):
    __tablename__ = 'ca_objects'

    id = Column(Integer, primary_key=True)
    sys_mon_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID системы мониторинга')
    sys_mon_object_id = Column(VARCHAR(50), comment='ID объекта в системе мониторинга')
    object_name = Column(VARCHAR(70), comment='Название объекта')
    object_status = Column(ForeignKey('object_statuses.status_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Статус объекта ссылается к статусам')
    object_add_date = Column(DateTime, comment='Дата добавления объекта')
    object_last_message = Column(DateTime, comment='Дата последнего сообщения')
    object_margin = Column(Integer, comment='Надбавка к базовой цене объекта')
    owner_contragent = Column(VARCHAR(200), comment='Хозяин контрагент')
    owner_user = Column(VARCHAR(255), comment='Хозяин юзер')
    imei = Column(VARCHAR(100), comment='идентификатор терминала')
    updated = Column(DateTime, comment='Когда изменён')
    object_created = Column(DateTime, comment='Дата создания в системе мониторинга ')
    parent_id_sys = Column(VARCHAR(200), comment='Id клиента в системе мониторинга')
    contragent_id = Column(ForeignKey('Contragents.ca_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    ca_uid = Column(String(100, 'utf8mb3_unicode_ci'), comment='Уникальный id контрагента')

    contragent = relationship('Contragents', back_populates='ca_objects')
    object_statuses = relationship('ObjectStatuses', back_populates='ca_objects')
    sys_mon = relationship('MonitoringSystem', back_populates='ca_objects')
    object_retranslators = relationship('ObjectRetranslators', back_populates='retr_object')
    object_sensors = relationship('ObjectSensors', back_populates='sensor_object')
    object_vehicles = relationship('ObjectVehicles', back_populates='vehicle_object')


class ClientsInSystemMonitor(Base):
    __tablename__ = 'clients_in_system_monitor'

    id = Column(Integer, primary_key=True)
    id_in_system_monitor = Column(VARCHAR(200), comment='Id клиента в системе мониторинга')
    name_in_system_monitor = Column(VARCHAR(200), comment='Имя клиента в системе мониторинга ')
    owner_id_sys_mon = Column(VARCHAR(200), comment='Id хозяина в системе мониторинга')
    system_monitor_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Id системы мониторинга ')
    client_id = Column(ForeignKey('Contragents.ca_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='id клиента')

    client = relationship('Contragents', back_populates='clients_in_system_monitor')
    system_monitor = relationship('MonitoringSystem', back_populates='clients_in_system_monitor')


class Devices(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    device_serial = Column(VARCHAR(100), comment='Серийный номер устройства')
    device_imei = Column(VARCHAR(60), comment='IMEI устройства')
    client_name = Column(String(300, 'utf8mb3_unicode_ci'), comment='Имя клиента')
    terminal_date = Column(DateTime, comment='Дата программирования терминала')
    devices_brand_id = Column(ForeignKey('devices_brands.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID Модели устройства ')
    name_it = Column(String(50, 'utf8mb3_unicode_ci'), comment='Имя програмировавшего терминал')
    sys_mon_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID системы мониторинга')
    contragent_id = Column(ForeignKey('Contragents.ca_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID контрагента')
    coment = Column(String(270, 'utf8mb3_unicode_ci'), comment='Коментарии')
    itprogrammer_id = Column(ForeignKey('auth_user.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)

    contragent = relationship('Contragents', back_populates='devices')
    devices_brand = relationship('DevicesBrands', back_populates='devices')
    itprogrammer = relationship('AuthUser', back_populates='devices')
    sys_mon = relationship('MonitoringSystem', back_populates='devices')
    sim_cards = relationship('SimCards', back_populates='sim_device')


class DevicesCommands(Base):
    __tablename__ = 'devices_commands'

    id = Column(Integer, primary_key=True)
    command = Column(VARCHAR(100))
    device_brand = Column(ForeignKey('devices_brands.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Id брэнда терминала')
    method = Column(VARCHAR(10))
    description = Column(VARCHAR(300))

    devices_brands = relationship('DevicesBrands', back_populates='devices_commands')


class ObjectRetranslators(Base):
    __tablename__ = 'object_retranslators'

    retranslator_id = Column(Integer, primary_key=True)
    retranslator_name = Column(VARCHAR(50))
    retranslator_suntel_price = Column(Integer)
    retranslator_ca_price = Column(Integer)
    retr_object_id = Column(ForeignKey('ca_objects.id'), index=True)

    retr_object = relationship('CaObjects', back_populates='object_retranslators')


class ObjectSensors(Base):
    __tablename__ = 'object_sensors'

    sensor_id = Column(Integer, primary_key=True)
    sensor_object_id = Column(ForeignKey('ca_objects.id'), index=True, comment='На каком объекте стоит по ID объекта')
    sensor_name = Column(VARCHAR(255), comment='Имя датчика в СМ')
    sensor_type = Column(VARCHAR(255), comment='Тип датчика(ДУТ, Температуры, наклона)')
    sensor_vendor = Column(VARCHAR(255), comment='производитель')
    sensor_vendor_model = Column(VARCHAR(255), comment='Модель датчика')
    sensor_serial = Column(VARCHAR(255), comment='Серийный номер датчика')
    sensor_mac_address = Column(VARCHAR(255), comment='Мак адрес датчика')
    sensor_technology = Column(VARCHAR(255), comment='Подтип датчика(аналоговый, цифровой, частотный)')
    sensor_connect_type = Column(VARCHAR(255), comment='Тип подключения')

    sensor_object = relationship('CaObjects', back_populates='object_sensors')


class ObjectVehicles(Base):
    __tablename__ = 'object_vehicles'

    vehicle_id = Column(Integer, primary_key=True)
    vehicle_object_id = Column(ForeignKey('ca_objects.id'), index=True)
    vehicle_ca_id = Column(ForeignKey('Contragents.ca_id'), index=True)
    vehicle_vendor_name = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_vendor_model = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_year_of_manufacture = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_gos_nomer = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_gos_nomer_region = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_type = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_vin = Column(String(255, 'utf8mb3_unicode_ci'))

    vehicle_ca = relationship('Contragents', back_populates='object_vehicles')
    vehicle_object = relationship('CaObjects', back_populates='object_vehicles')


class SimCards(Base):
    __tablename__ = 'sim_cards'

    sim_id = Column(Integer, primary_key=True)
    sim_iccid = Column(VARCHAR(40), comment='ICCID')
    sim_tel_number = Column(VARCHAR(40), comment='телефонный номер сим')
    client_name = Column(VARCHAR(270), comment='Имя клиента')
    sim_cell_operator = Column(ForeignKey('Cell_operator.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Сотовый оператор(надо по ID)')
    sim_owner = Column(TINYINT(1), comment='Владелец сим (мы или клиент)')
    sim_device_id = Column(ForeignKey('devices.device_id'), index=True, comment='ID к девайсам(devices)')
    sim_date = Column(DateTime, comment='Дата регистрации сим')
    status = Column(Integer, comment='Активность симки:\\r\\n0-списана, 1-активна, 2-приостан')
    terminal_imei = Column(String(25, 'utf8mb3_unicode_ci'), comment='IMEI терминала в который вставлена симка')
    contragent_id = Column(ForeignKey('Contragents.ca_id', ondelete='SET NULL', onupdate='SET NULL'), index=True, comment='ID контрагента')
    ca_uid = Column(String(100, 'utf8mb3_unicode_ci'), comment='Уникальный id контрагента')
    itprogrammer_id = Column(ForeignKey('auth_user.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID сотрудника програмировавшего терминал')

    contragent = relationship('Contragents', back_populates='sim_cards')
    itprogrammer = relationship('AuthUser', back_populates='sim_cards')
    Cell_operator = relationship('CellOperator', back_populates='sim_cards')
    sim_device = relationship('Devices', back_populates='sim_cards')
