# coding:utf-8

# 存放项目的模型
from datetime import datetime

# 导入SQLAlchemy模块
from bluelog.utils.extensions import db


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    deal_number = db.Column(db.String(200))
    income_expense = db.Column(db.String(20))
    logic1=db.Column(db.Integer)
    deal_date = db.Column(db.DateTime)
    money = db.Column(db.Float)
    count_type_f = db.Column(db.String(50))
    count_type_s = db.Column(db.String(50))
    pay_status = db.Column(db.String(20))
    logic2 = db.Column(db.Integer)
    deal_type = db.Column(db.String(20))
    counterparty = db.Column(db.String(50))
    goods = db.Column(db.String(300))
    deal_source = db.Column(db.String(50))
    amount = db.Column(db.Float)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
