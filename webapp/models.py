#coding:utf-8
# 存放项目的模型
from datetime import datetime

# 导入SQLAlchemy模块
from flask_sqlalchemy import SQLAlchemy
# 初始化db
db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    u_id = db.Column(db.Integer, autoincrement=True，primary_key=True)
    username = db.Column(db.String(16),unique=True)
    password = db.Column(db.String(250))
    
