# coding:utf-8
from bluelog.utils.extensions import db
from flask_login import UserMixin


# 存储用户信息的数据库模型类
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))  # 用户名
    access_token = db.Column(db.String(200))  # 授权完成后获取的访问令牌

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

