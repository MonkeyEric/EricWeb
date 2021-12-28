# coding:utf-8


from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy_utils.types.choice import ChoiceType

#  创建对象的基类
Base = declarative_base()
types_choices = (
    (0, '可访问'),
    (1, '可授权'),
)


class TestUser(Base):
    __tablename__ = 'testUser'
    user_id = Column("user_id", INTEGER, primary_key=True, nullable=False, autoincrement=True)
    login_name = Column('login_name', type_=String(64), nullable=False)
    password = Column('password', type_=String(64), nullable=False)
    username = Column('username', type_=String(64), nullable=False)
    mobile = Column('mobile', type_=String(64))
    email = Column('email', type_=String(64))
    gen_time = Column('gen_time', DateTime)
    login_time = Column('login_time', DateTime)
    last_login_time = Column(DateTime, server_default=func.now())
    count = Column('count', INTEGER, nullable=False)


# 定义对象，与元数据相对应
class User(Base):  # ok
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    user_id = Column("user_id", INTEGER, primary_key=True, nullable=False, autoincrement=True)
    org_id = Column(INTEGER, ForeignKey("org.org_id"), nullable=False)
    login_name = Column('login_name', type_=String(64), nullable=False)
    password = Column('password', type_=String(64), nullable=False)
    username = Column('username', type_=String(64), nullable=False)
    mobile = Column('mobile', type_=String(64))
    email = Column('email', type_=String(64))
    gen_time = Column('gen_time', DateTime)
    login_time = Column('login_time', DateTime)
    last_login_time = Column(DateTime, server_default=func.now())
    count = Column('count', INTEGER, nullable=False)


class Right(Base):  # ok
    __tablename__ = 'right'
    right_id = Column(INTEGER, nullable=False, primary_key=True)
    parent_tr_id = Column(INTEGER, nullable=False)
    right_name = Column(type_=String(64), nullable=False)
    description = Column(type_=String(64))


class Role(Base):  # ok
    __tablename__ = 'role'
    role_id = Column(INTEGER, nullable=False, primary_key=True)
    parent_tr_id = Column(INTEGER, nullable=False)
    role_name = Column(type_=String(64), nullable=False)
    gen_time = Column(DateTime, nullable=False)
    description = Column(type_=String(64))


class Log(Base):  # ok
    __tablename__ = 'log'

    log_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    op_type = Column(INTEGER, nullable=False)
    content = Column(type_=String(64), nullable=False)
    user_id = Column(ForeignKey('user.user_id'), nullable=False)
    gen_time = Column(DateTime, nullable=False)


class Org(Base):  # ok
    __tablename__ = 'org'
    org_id = Column(INTEGER, nullable=False, primary_key=True)
    parent_to_id = Column(INTEGER, nullable=False)
    org_name = Column(type_=String(64), nullable=False)
    gen_time = Column(DateTime, server_default=func.now())
    description = Column(type_=String(64))


class UserGroup(Base):  # ok
    __tablename__ = 'userGroup'
    u_group_id = Column(INTEGER, nullable=False, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('user.user_id'), nullable=False)
    group_id = Column(INTEGER, ForeignKey('group.group_id'), nullable=False)


class Group(Base):  # ok
    __tablename__ = 'group'
    group_id = Column(INTEGER, nullable=False, primary_key=True)
    group_name = Column(type_=String(64), nullable=False)
    parent_tg_id = Column(INTEGER, nullable=False)
    gen_time = Column(DateTime, server_default=func.now())
    description = Column(type_=String(64))


class UserRole(Base):  # ok
    __tablename__ = 'userRole'
    u_role_id = Column(INTEGER, nullable=False, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('user.user_id'), nullable=False)
    role_id = Column(INTEGER, ForeignKey('role.role_id'), nullable=False)


class UserRight(Base):
    __tablename__ = 'userRight'
    global types_choices
    u_right_id = Column(INTEGER, nullable=False, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False)
    right_id = Column(ForeignKey('right.right_id'), nullable=False)
    right_type = Column(ChoiceType(types_choices), nullable=False)


class GroupRight(Base):
    __tablename__ = 'groupRight'
    global types_choices
    g_right_id = Column(INTEGER, nullable=False, primary_key=True)
    group_id = Column(INTEGER, ForeignKey('group.group_id'), nullable=False)
    right_id = Column(INTEGER, ForeignKey('right.right_id'), nullable=False)
    right_type = Column(ChoiceType(types_choices), nullable=False)


class GroupRole(Base):
    __tablename__ = 'groupRole'
    g_role_id = Column(INTEGER, nullable=False, primary_key=True)
    group_id = Column(INTEGER, ForeignKey('group.group_id'), nullable=False)
    role_id = Column(INTEGER, ForeignKey('role.role_id'), nullable=False)


class RoleRight(Base):
    __tablename__ = 'roleRight'
    global types_choices
    role_right_id = Column(INTEGER, nullable=False, primary_key=True)
    role_id = Column(ForeignKey('role.role_id'), nullable=False)
    right_id = Column(ForeignKey('right.right_id'), nullable=False)
    right_type = Column(ChoiceType(types_choices), nullable=False)


# 初始化数据库链接:
engine = create_engine('mysql+pymysql://root:Zjq;;123456@localhost:3306/my_web')
Base.metadata.create_all(engine)  # 创建表结构
# DB_session
DB_session = sessionmaker(bind=engine)

# 创建session对象
session = DB_session()

# 创建User对象
new_user = TestUser(user_id=512314, login_name='1649107451@qq.com', passowrd='1234556',
                    username='Eric', mobile='1233465668', email='12310249@qq.com', gen_time=func.now(),
                    login_time=func.now(),
                    last_login_time=func.now(), count=12)

# 添加到session
session.add(new_user)

# 提交即保存到数据库
session.commit()

# 关闭session
session.close()
