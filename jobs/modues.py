import os
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__).replace("\jobs",""), '.env')

load_dotenv(dotenv_path=dotenv_path)
print('123123',os.getenv("SQLALCHEMY_DATABASE_URI"))
engine = create_engine(
    os.getenv("SQLALCHEMY_DATABASE_URI"),
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    avatar = Column(String(150))
    web_url = Column(String(150))
    name = Column(String(30))
    express = Column(String(200))
    thumb_down = Column(Integer, default=0)
    category = Column(String(30))
    thumb_up = Column(Integer, default=0)
    update_time = Column(DateTime, default=datetime.now())
