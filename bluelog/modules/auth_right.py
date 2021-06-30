# coding:utf-8


from sqlalchemy import Column,String,create_engine,INTEGER,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exy.delarative import declarative_base
from sqlalchemy.sql import func
#  创建对象的基类
Base = declarative_base()
types_choices = (
                (0,'可访问'),
                (1,'可授权'),
                )
# 定义对象，与元数据相对应
class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    user_id = Column("user_id",INTEGER,primary_key=True,nullable=False,autoincrement=True)
    org_id = Column('org_id',INTEGER,nullable=False,ForeignKey("org.org_id"))
    login_name = Column('login_name',String,nullable=False)
    passowrd = Column('password',String,nullable=False)
    username = Column('username',type_=String(length=32),nullbale=False)
    mobile = Column('mobile',String)
    email = Column('email',String)
    gen_time = Column('gen_time',)
    login_time = Column('login_time',DateTime)
    last_login_time = Column('last_login_time',server_default=func.now())
    count = Column('count',INTEGER,nullable=False)
    
class Log(Base):
    __tablename__ = 'log'

    log_id = Column(INTEGER,nullable=False,primary_key=True,autoincrement=True)
    op_type = Column('op_type',INTEGER,nullable=False)
    content = Column('content',type_=String(length=64),nullable=False)
    user_id = Column(nullable=False,ForeignKey('user.user_id'))
    gen_time = Column(DateTime,nullable=False)


class Org(Base):
    __tablename__ = 'org'
    org_id = Column(INTEGER,nullable=False,primary_key=True)
    parent_to_id = Column(INTEGER,nullable=False)
    org_name = Column(type_=String(length=64),nullable=False)
    gen_time = Column(DateTime,server_default=func.now())
    description = Column(type_=String(length=64)

class UserGroup(Base):
    __tablename__ = 'userGroup'
    ugroup_id = Column(INTEGER,nullable=False,primary_key=True)
    user_id = Column(INTEGER,nullable=False,ForeignKey('user.user_id'))
    group_id = Column(INTEGER,nullable=False,ForeignKey('group.group_id'))

class Group(Base):
    __tablename__ = 'group'
    group_id = Column(INTEGER,nullable=False,primary_key=True)
    group_name = Column(type_=String(length=64),nullable=False)
    parent_tg_id = Column(INTEGER,nullable=False,nullable=False)
    gen_time = Column(DateTime,server_default=func.now())
    description = Column(type_=String(length=64))

class UserRole(Base):
    __tablename__ = 'userRole'
    urole_id = Column(INTEGER,nullable=False,primary_key=True)
    user_id = Column(INTEGER,nullable=False,ForeignKey('user.user_id'))
    role_id = Column(INTEGER,nullable=False,ForeignKey('role.role_id'))

class UserRight(Base):
    __tablename__ = 'userRight'
    uright_id = Column(INTEGER,nullable=False,primary_key=True)
    user_id = Column(INTEGER,nullable=False,ForeignKey('user.user_id'))
    right_id = Column(INTEGER,nullable=False,ForeignKey('role.role_id'))    
    right_type = Column(nullable=False,ChoiceType(types_choices,Integer()))


class GroupRight(Base):
    gright_id = Column(INTEGER,nullable=False,primary_key=True)
    group_id = Column(INTEGER,nullable=False,ForeignKey('group.group_id'))
    right_id = Column(INTEGER,nullable=False,ForeignKey('right.right_id'))
    right_type = Column(nullable=False,ChoiceType(types_choices,Integer()))

class RoleRight(Base):
    __tablename__ = 'roleRight'
    role_right_id = Column(INTEGER,nullable=False,primary_key=True)
    role_id = Column(nullable=False,ForeignKey('role.role_id'))
    right_id = Column(nulable=False,ForeignKey('right.right_id'))
    rught_tye
# 初始化数据库链接:
engine = create_engine('mysql+mysqlconnector://root:Zjq;;123456@localhost:3306/my_web')

# 创建DBsession类型
DBsession = sessionmaker(bind=engine)

# 创建session对象
session = DBsession()

# 创建User对象
new_user = User()

# 添加到session
session.add()

# 提交即保存到数据库
session.commit()

# 关闭session
session.close()

