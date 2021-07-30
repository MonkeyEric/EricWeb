# coding:utf-8
from bluelog.config import *
from bluelog.utils.extensions import db
from bluelog.modules.income_expense import Income
from datetime import datetime
import csv

import json


def read_csv(filename, desc):
    """
    输入文件，返回json的格式
    :param filename:
    :param desc:
    :return:
    """
    table_data = []
    deal_source = ''
    with open(filename, 'r') as file:
        if '支付宝' in desc:
            csv_data = csv.DictReader(file, fieldnames=Alipay_head.values())
            deal_source = 'alipay'
        else:
            csv_data = csv.DictReader(file, fieldnames=Wechat_head.values())
            deal_source = 'wechat'
        for row in csv_data:
            # 读取的内容是字典格式的
            if row.get('deal_number').isdigit():
                row['deal_source'] = deal_source
                table_data.append(dict(row))

        return table_data


def save_to_db(data):
    for i in data:
        if i.get('deal_number'):
            income_result = Income.query.filter_by(deal_number=i.get('deal_number'))
            if not income_result.count():
                if i.get('income_expense') == '支出':
                    i['logic1'] = -1
                elif i.get('income_expense') == '收入':
                    i['logic1'] = 1
                else:
                    i['logic1'] = 0
                if i.get('pay_status') in ["支付成功","交易成功","已转账","已存入零钱","已收钱"]:
                    i['logic2'] = 1
                else:
                    i['logic2'] = 0
                i['amount'] = round(i['logic2']*i['logic1']*float(i.get('money')),2)
                income = Income(
                    deal_number=i.get('deal_number'),
                    income_expense=i.get('income_expense'),
                    logic1=i.get('logic1'),
                    logic2=i.get('logic2'),
                    deal_date=i.get('deal_date'),
                    money=i.get('money'),
                    count_type=i.get('count_type'),
                    pay_status=i.get('pay_status'),
                    deal_type=i.get('deal_type'),
                    counterparty=i.get('counterparty'),
                    goods=i.get('goods'),
                    deal_source=i.get('deal_source'),
                    amount=i.get('amount'),
                )
                db.session.add(income)
                db.session.commit()
                print('insert success')


def count_type_ai(name_str):
    pass