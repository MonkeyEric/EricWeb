# coding:utf-8
import csv
import datetime
from functools import reduce
from bluelog.config_dict import *
from datetime import datetime
from collections import Counter
import pandas as pd
import time
import pymongo
import json
import qd_suanfa2

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn['online']
qd_report_data = db['qd_report_data']


def read_csv(filename):
    """
    输入文件，返回json的格式
    :param filename:
    :return:
    """
    table_data = []
    deal_source = ''
    with open(filename, 'r') as file:
        csv_data = csv.DictReader(file, fieldnames=channel_head.values())
        # filename=["是否计算收益率贡献", "理财师", "客户姓名", "币种", "标的", "交割日期", "投资净值", "买入份额", "总出资金额",
        #                                             "客户卖出时间", "客户退出净值", "费前收益", "前端佣金", "上期单位净值", "最新单位净值/最新收盘价"]
        for row in csv_data:
            # 读取的内容是字典格式的
            if row.get('investment_net') != '0' and row.get('investment_net') != '投资净值':
                row['investment_net'] = round(float(row['investment_net']),2)
                row['buy_share'] =int(row['buy_share']) if r"DIV/0" not in row['buy_share'] else 0
                row['investment_amount'] = round(float(row['investment_amount']),2)
                row['exit_fee'] = round(float(row['exit_fee']), 2)
                row['fee_earnings_before'] = round(float(row['fee_earnings_before']), 2)
                row['front_rate'] = round(float(row['front_rate']), 2)
                row['backend_rate'] = round(float(row['backend_rate']), 2)
                row['customer_profit'] = round(row['exit_fee'] - row['investment_amount'] if row['exit_fee'] > 0 else 0,2)  #
                # if row.get('delivery_time'):
                #     row['delivery_time'] = datetime.strptime(row.get('delivery_time'), '%Y/%m/%d')
                if row.get('sale_time'):
                    if row['sale_time'] == '1900/1/0':
                        row['sale_time'] = '-'
                    # else:
                    #     row['sale_time'] = datetime.strptime(row.get('sale_time'), '%Y/%m/%d')

                table_data.append(dict(row))

        return table_data


def change_rate(nums, s_currency, d_currency, rate):
    nums = float(nums)
    if s_currency == 'USD':
        if d_currency == 'CNY':
            nums = nums * float(rate.get('USD_CNY'))
        elif d_currency == 'HKD':
            nums = nums * float(rate.get('USD_HKD'))
    elif s_currency == 'HKD':
        if d_currency == 'USD':
            nums = nums * float(1) / float(rate.get('USD_HKD'))
        elif d_currency == 'CNY':
            nums = nums * float(1) / float(rate.get('CNY_HKD'))
    elif s_currency == 'CNY':
        if d_currency == 'USD':
            nums = nums * float(1) / float(rate.get('USD_CNY'))
        elif d_currency == 'HKD':
            nums = nums * float(rate.get('CNY_HKD'))
    return round(nums, 2)


def channel_report_logic(report_data, request_dict):
    # 每行的数据
    rate_note = False  # 默认不显示汇率注释
    # exchange_rate是一个dict，包含USD HKD
    currency = request_dict.get('currency')
    channel_name = request_dict.get('channel_name')
    report_date = request_dict.get('report_date')
    rate = request_dict.get('exchange_rate')
    # 转换币种
    new_dict =[]
    for i in report_data:
        # i['investment_net'] = round(float(i.get('investment_net')), 2)  # 投资净值
        # i['buy_share'] = int(i.get('investment_net'))  # 买入份额
        # i['exit_fee'] = round(float(i.get('exit_fee')), 2)  # 退出净值
        # i['front_rate'] = round(float(i.get('front_rate')), 2)  # 前端佣金
        # i['backend_rate'] = round(float(i.get('backend_rate')), 2)  # 后端佣金
        # i['investment_amount'] = round(float(i.get('investment_amount')), 2)
        # i['last_netvalue'] = round(float(i.get('last_netvalue')), 2)  # 上期单位净值
        # i['fee_earnings_before'] = round(float(i.get('fee_earnings_before')), 2)  # 费前收益
        # i['customer_profit'] =round(i['exit_fee'] - i['investment_amount'] if i['exit_fee'] > 0 else 0,2) # 客户盈利
        i['customer_name'] = i['customer_name'].upper()
        if i.get('currency_type') != currency:
            # 重新计算
            rate_note = True
            # 总出资金额
            i['investment_amount'] = change_rate(i.get('investment_amount'), i.get('currency_type'), currency, rate)
            # 退出净值
            i['exit_fee'] = change_rate(i.get('exit_fee'), i.get('currency_type'), currency, rate)
            # 前端佣金
            i['front_rate'] = change_rate(i.get('front_rate'), i.get('currency_type'), currency, rate)
            # 后端佣金
            i['backend_rate'] = change_rate(i.get('backend_rate'), i.get('currency_type'), currency, rate)
            # 投资净值
            i['investment_net'] = change_rate(i.get('investment_net'), i.get('currency_type'), currency, rate)
            # 费钱收益
            i['fee_earnings_before'] = change_rate(i.get('fee_earnings_before'), i.get('currency_type'), currency, rate)
            i['customer_profit'] = round(i['exit_fee'] - i['investment_amount'] if i['exit_fee'] > 0 else 0,2)  #
        i['total_rate'] = i['front_rate'] + i['backend_rate']
        new_dict.append(i)

    # 覆盖客户情况
    customer_num = len({i.get('customer_name') for i in new_dict})
    total_invest = reduce(lambda x, y: x + y, [i['investment_amount'] for i in new_dict])
    # 人均投资总额
    per_investment = round(float(total_invest) / float(customer_num),2)
    # 客单价
    customer_unit_price = round(float(total_invest) / float(len(new_dict)),2)
    # 总盈利金额
    total_profit = reduce(lambda x, y: x + y, [i['customer_profit'] for i in new_dict])
    per_profit = round(float(total_profit) / float(customer_num),2)
    # 佣金收益情况
    total_rate = reduce(lambda x, y: x + y, [i['total_rate'] for i in new_dict])
    # 前端佣金
    front_rate = reduce(lambda x, y: x + y, [i['front_rate'] for i in new_dict])
    # 后端佣金
    backend_rate = reduce(lambda x, y: x + y, [i['backend_rate'] for i in new_dict])
    # 图表1
    chart_data = {}
    for index,i in enumerate(new_dict):
        chart_data[index] = i
    df = pd.read_json(json.dumps(chart_data), orient='index')

    # 盈利按客户
    res1 =json.loads((df.groupby('customer_name')['customer_profit'].sum()).to_json(orient='split'))
    profit_customer = res1
    profit_customer_top3 =[name[0] for name in sorted(zip(res1['index'], res1['data']),key=lambda x:x[1],reverse=True)][:3]
    del res1
    # 盈利按标的
    res2 = json.loads((df.groupby('investment_target')['customer_profit'].sum()).to_json(orient='split'))
    profit_invest = res2
    profit_invest_top3 = [name[0] for name in sorted(zip(res2['index'], res2['data']),key=lambda x:x[1],reverse=True)][:3]
    del res2
    # 佣金按客户
    res3 = json.loads((df.groupby('customer_name')[['front_rate','backend_rate']].sum()).to_json(orient='columns'))
    rate_customer = {key:list(value.values()) for key,value in res3.items()}
    rate_customer['index'] = list(res3['front_rate'].keys())
    rate_customer_top3 =[i[0]for i in sorted(dict(Counter(res3['front_rate'])+Counter(res3['backend_rate'])).items(),key=lambda x:x[1],reverse=True)][:3]

    del res3
    # 佣金按标的
    res4 = json.loads((df.groupby('investment_target')[['front_rate', 'backend_rate']].sum()).to_json(orient='columns'))
    rate_invest = {key1: list(value1.values()) for key1, value1 in res4.items()}
    rate_invest['index'] = list(res4['front_rate'].keys())
    rate_invest_top3 =[i[0]for i in sorted(dict(Counter(res4['front_rate'])+Counter(res4['backend_rate'])).items(),key=lambda x:x[1],reverse=True)][:3]
    del res4
    # 最后传输的数据
    report_json = {
        'lcs_name': channel_name,
        'currency_type': currency,
        'report_date': report_date,
        'customer_num':customer_num,
        'total_invest':total_invest,
        'per_investment':per_investment,
        'customer_unit_price':customer_unit_price,
        'per_profit':per_profit,
        'total_profit':total_profit,
        'front_rate':front_rate,
        'backend_rate':backend_rate,
        'total_rate':total_rate,
        'rate_note':rate_note,
        'profit_customer':profit_customer,
        'profit_customer_top3':profit_customer_top3,
        'profit_invest':profit_invest,
        'profit_invest_top3':profit_invest_top3,
        'rate_customer':rate_customer,
        'rate_customer_top3':rate_customer_top3,
        'rate_invest':rate_invest,
        'rate_invest_top3':rate_invest_top3
    }
    print(report_json)

    # 是否计算收益率贡献
    # yield_status = i.get('yield_status')
    # lcs_name = i.get('lcs_name')
    # customer_name = i.get('customer_name')
    # currency_type = i.get('currency_type')
    # # 标的
    # investment_target = i.get('investment_target')
    # # 交割日期
    # delivery_time = i.get('delivery_time')
    # # 卖出时间
    # sale_time = i.get('sale_time')
    # # 最新单位净值 / 最新收盘价
    # new_netvalue = i.get('new_netvalue')

    return report_json


def main():
    request_dict = {
        'channel_id': '',
        'channel_name': '张三',
        'currency': 'USD',
        'exchange_rate': {'USD_HKD': '7.75', 'USD_CNY': '6.50', 'CNY_HKD': '1.20'},
        'report_date': datetime.now()
    }
    report_data = qd_report_data.find({'lcs_name': request_dict.get('channel_name')},{'_id':0})
    result = channel_report_logic(report_data, request_dict)
    print('1',result)
    # result1 = qd_suanfa2.channel_report_logic(report_data,'张三', 'USD', '7.75', '6.50', '1.20')
    # print('1', result1)


if __name__ == '__main__':
    # report_data = read_csv('qdjl.csv')
    # for i in report_data:
    #     qd_report_data.insert_one(i)
    # planB 和正常程序进行pK时间
    # # 存储数据，插入没有的数据
    #     pool = ThreadPool(5)  # 创建一个线程池
    #     a = [(a, orgId) for a in ResponseData['rows']]
    #     pool.map(store_data, a)  # 往线程池中填线程
    #     pool.close()  # 关闭线程池，不再接受线程
    #     pool.join()
    begin_time = time.time()
    main()
    end_time = time.time()
    print('该循环程序运行时间:',(end_time-begin_time))
    # y ={"1":{"a":3,"b":4,"c":2},"0":{"a":1,"b":2,"c":12},"2":{"a":1,"b":4,"c":8}}
    # df = pd.read_json(json.dumps(y),orient='index')
    # res1 =df.groupby('a')[['b','c']].sum()
    # print(df)
    # print(res1)
    # print(res1.to_json(orient='columns'))

    # 排序需要前3个的客户以及标的
    # 给前端的数据是按照姓名或者标的排序的
    # {"b":{"1":6,"3":4},"c":{"1":20,"3":2}}  columns

