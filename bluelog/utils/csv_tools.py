# coding:utf-8
from bluelog.money_excel_model import *
from bluelog.utils.extensions import db
from bluelog.modules.income_expense import Income
import pandas as pd


def read_csv(filename, desc):
    """
    输入文件，返回json的格式
    :param filename:
    :param desc:
    :return:
    """
    table_data = []
    deal_source = ''
    # 读
    if '支付宝' in desc or '微信' in desc:
        if '支付宝' in desc:
            deal_source = 'alipay'
        elif '微信' in desc:
            deal_source = 'wechat'
        xl = pd.read_excel(filename, header=None, names=alipay_head.values(), skiprows=1)
        for row in xl.to_dict(orient="records"):
            # 读取的内容是字典格式的
            try:
                if row.get('deal_number').isdigit():
                    if deal_source:
                        row['deal_source'] = deal_source
                    table_data.append(dict(row))
            except Exception as e:
                print(e)
                continue
        return table_data
    else:
        xl = pd.read_excel(filename, header=None, names=detail_head.values(), skiprows=1)
        try:
            for row in xl.to_dict(orient="records"):
                # 读取的内容是字典格式的
                if row.get('money') != '金额':
                    if deal_source:
                        row['deal_source'] = deal_source
                    table_data.append(dict(row))
        except Exception as e:
            print('@@@@@@@@', e)
        finally:
            return table_data


def save_to_db(data, owner_id):
    for i in data:
        try:
            if i.get('deal_number'):
                income_result = Income.query.filter_by(deal_number=i.get('deal_number'), deal_date=i.get('deal_date'))
                if not income_result.count():
                    # i['money'] = float(i.get('money').replace('￥', ''))
                    if i.get('income_expense') == '支出':
                        i['logic1'] = -1
                    elif i.get('income_expense') == '收入':
                        i['logic1'] = 1
                    else:
                        i['logic1'] = 0
                    if i.get('pay_status') in ["支付成功", "交易成功", "已转账", "已存入零钱", "已收钱"]:
                        i['logic2'] = 1
                    else:
                        i['logic2'] = 0
                    i['amount'] = round(i['logic2'] * i['logic1'] * float(i.get('money')), 2)
                    if not i.get('count_type'):
                        count_type_f = ''
                        count_type_s = ''
                    else:
                        count_type_s = i.get('count_type').split('-')[1] if i.get('count_type') != '非必需品' else '非必需品',
                        count_type_f = i.get('count_type').split('-')[0] if i.get('count_type') != '非必需品' else '非必需品',
                    income = Income(
                        deal_number=i.get('deal_number'),
                        income_expense=i.get('income_expense'),
                        logic1=i.get('logic1'),
                        logic2=i.get('logic2'),
                        deal_date=i.get('deal_date'),
                        money=i.get('money'),
                        count_type_s=count_type_s,
                        count_type_f=count_type_f,
                        pay_status=i.get('pay_status'),
                        deal_type=i.get('deal_type'),
                        counterparty=i.get('counterparty'),
                        goods=i.get('goods'),
                        deal_source=i.get('deal_source'),
                        amount=i.get('amount'),
                        owner_id=owner_id
                    )
                    db.session.add(income)
                    db.session.commit()
        except Exception as e:
            print(e)
            continue
