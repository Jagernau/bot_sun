from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKey, Identity, Integer, Numeric, SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name = Column(String(150), nullable=False, unique=True)

    auth_user_groups = relationship('AuthUserGroups', back_populates='group')
    auth_group_permissions = relationship('AuthGroupPermissions', back_populates='group')


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    password = Column(String(128), nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(True), nullable=False)
    last_login = Column(DateTime(True))

    auth_user_groups = relationship('AuthUserGroups', back_populates='user')
    authtoken_token = relationship('AuthtokenToken', uselist=False, back_populates='user')
    django_admin_log = relationship('DjangoAdminLog', back_populates='user')
    auth_user_user_permissions = relationship('AuthUserUserPermissions', back_populates='user')


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        UniqueConstraint('app_label', 'model'),
    )

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

    auth_permission = relationship('AuthPermission', back_populates='content_type')
    django_admin_log = relationship('DjangoAdminLog', back_populates='content_type')


class DjangoMigrations(Base):
    __tablename__ = 'django_migrations'

    id = Column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime(True), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True, index=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime(True), nullable=False, index=True)


t_foremail = Table(
    'foremail', metadata,
    Column('Контрагент', Text),
    Column('ИНН', Text),
    Column('КПП', Text),
    Column('Тариф', Numeric),
    Column('Коэффициент тарифа', Numeric)
)


class Tagat(Base):
    __tablename__ = 'tagat'
    __table_args__ = {'comment': 'Дополнительная разбивка одной учетной записи по ИНН. Впервые '
                'возникла необходимость для агат-проекта'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('tagat_id_seq'::regclass)"))
    object = Column(Text)
    idobject = Column(Text)
    shortname = Column(Text)
    inn = Column(Text)
    tarif = Column(Numeric)
    idsystem = Column(BigInteger)
    kpp = Column(Text)
    name = Column(Text)
    dbeg = Column(DateTime)
    dend = Column(DateTime)


class Tdata(Base):
    __tablename__ = 'tdata'

    id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    login = Column(Text)
    idlogin = Column(Text)
    idsystem = Column(Integer)
    object = Column(Text)
    idobject = Column(Text)
    isactive = Column(Text)
    dimport = Column(DateTime)


class Temail(Base):
    __tablename__ = 'temail'

    id = Column(Integer, primary_key=True, server_default=text("nextval('temail_id_seq'::regclass)"))
    email = Column(Text)
    name = Column(Text)
    inn = Column(Text)
    kpp = Column(Text)


class Tklient(Base):
    __tablename__ = 'tklient'

    id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name = Column(Text)
    shortname = Column(Text)
    type = Column(Text)
    inn = Column(Text)
    kpp = Column(Text)
    tarif = Column(Numeric)

    ttarif = relationship('Ttarif', back_populates='tklient')


t_tsveta = Table(
    'tsveta', metadata,
    Column('name', Text),
    Column('skol', Numeric),
    Column('kol1', Numeric),
    Column('kol2', Numeric),
    Column('tar1', Numeric),
    Column('tar2', Numeric),
    Column('sum', Numeric),
    Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), nullable=False),
    comment='для проставки тарифов в таблицу tklient, вспомогательная'
)


class Twialon100(Base):
    __tablename__ = 'twialon100'
    __table_args__ = {'comment': 'Таблица учетных записей Клиента. Исторически сформированная на '
                'основания Google таблицы Wialon100. Является вспомогательной '
                'таблицей для соединения объекта мониторинга и клиента.'}

    id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    klient = Column(Text)
    login = Column(Text)
    logintd = Column(Text)
    tkid = Column(BigInteger)


t_vdubles = Table(
    'vdubles', metadata,
    Column('goznak', Text),
    Column('count', BigInteger)
)


t_vtofind = Table(
    'vtofind', metadata,
    Column('login', Text)
)


t_vwialon = Table(
    'vwialon', metadata,
    Column('login', Text),
    Column('count', BigInteger)
)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        UniqueConstraint('content_type_id', 'codename'),
    )

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    codename = Column(String(100), nullable=False)

    content_type = relationship('DjangoContentType', back_populates='auth_permission')
    auth_group_permissions = relationship('AuthGroupPermissions', back_populates='permission')
    auth_user_user_permissions = relationship('AuthUserUserPermissions', back_populates='permission')


class AuthUserGroups(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id'),
    )

    id = Column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    group_id = Column(ForeignKey('auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    group = relationship('AuthGroup', back_populates='auth_user_groups')
    user = relationship('AuthUser', back_populates='auth_user_groups')


class AuthtokenToken(Base):
    __tablename__ = 'authtoken_token'

    key = Column(String(40), primary_key=True, index=True)
    created = Column(DateTime(True), nullable=False)
    user_id = Column(ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, unique=True)

    user = relationship('AuthUser', back_populates='authtoken_token')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('action_flag >= 0'),
    )

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    action_time = Column(DateTime(True), nullable=False)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SmallInteger, nullable=False)
    change_message = Column(Text, nullable=False)
    user_id = Column(ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    object_id = Column(Text)
    content_type_id = Column(ForeignKey('django_content_type.id', deferrable=True, initially='DEFERRED'), index=True)

    content_type = relationship('DjangoContentType', back_populates='django_admin_log')
    user = relationship('AuthUser', back_populates='django_admin_log')


class Ttarif(Base):
    __tablename__ = 'ttarif'

    id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    tkid = Column(ForeignKey('tklient.id'))
    tarif = Column(Numeric)
    dbeg = Column(DateTime)
    dend = Column(DateTime)

    tklient = relationship('Tklient', back_populates='ttarif')


class AuthGroupPermissions(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        UniqueConstraint('group_id', 'permission_id'),
    )

    id = Column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    group_id = Column(ForeignKey('auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    permission_id = Column(ForeignKey('auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    group = relationship('AuthGroup', back_populates='auth_group_permissions')
    permission = relationship('AuthPermission', back_populates='auth_group_permissions')


class AuthUserUserPermissions(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        UniqueConstraint('user_id', 'permission_id'),
    )

    id = Column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    permission_id = Column(ForeignKey('auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    permission = relationship('AuthPermission', back_populates='auth_user_user_permissions')
    user = relationship('AuthUser', back_populates='auth_user_user_permissions')
