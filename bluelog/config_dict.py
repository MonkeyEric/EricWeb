# coding:utf-8

channel_head = {
    '是否计算收益率贡献': 'yield_status',
    '理财师': 'lcs_name',
    '客户姓名': 'customer_name',
    '币种': 'currency_type',
    '标的': 'investment_target',
    '交割日期': 'delivery_time',
    '投资净值': 'investment_net',
    '买入份额': 'buy_share',
    '总出资金额': 'investment_amount',
    '客户卖出时间': 'sale_time',
    '客户退出净值': 'exit_fee',
    '费前收益': 'fee_earnings_before',
    '前端佣金': 'front_rate',
    '后端佣金': 'backend_rate',
    '上期单位净值': 'last_netvalue',
    '最新单位净值/最新收盘价': 'new_netvalue'
}

Wechat_head = {
    '交易时间': 'deal_date',
    '交易类型': 'deal_type',
    '交易对方': 'counterparty',
    '商品': 'goods',
    '收支': 'income_expense',
    '金额': 'money',
    '支付方式': 'pay_way',
    '当前状态': 'pay_status',
    '交易单号': 'deal_number',
    '商户单号': 'merchants_order',
    '备注': 'note'
}

Alipay_head = {
    '交易号': 'deal_number',
    '商家订单': 'merchants_order',
    '交易创建': 'deal_date',
    '付款时间': 'pay_date',
    '最近修改时间': 'update_date',
    '交易来源': 'deal_source',
    '类型': 'deal_type',
    '交易对方': 'counterparty',
    '商品名称': 'goods',
    '金额': 'money',
    '收支': 'income_expense',
    '交易状态': 'pay_status',
    '服务费': 'service_money',
    '成功退款': 'refund',
    '备注': 'note',
    '资金状态': 'money_status'
}

detail_head = {
    '交易号': 'deal_number',
    '交易时间': 'deal_date',
    '收/支': 'income_expense',
    '金额': 'money',
    '统计种类': 'count_type',
    '交易状态': 'pay_status',
    '交易类型': 'deal_type',
    '交易对方': 'counterparty',
    '商品': 'goods',
    '交易来源': 'deal_source',

}

Table_head = {
    'deal_date': '交易时间',
    'income_expense': '收支',
    'amount': '金额',
    'count_type': '统计种类',
    'pay_status': '支付状态',
    'counterparty': '交易对方',
    'goods': '商品名称',
}

Expense_type = {
    '餐饮': [
        '吃饭',
        '外卖',
        '水果',
        '零食/饮料/酒',
        '乳制品',
        '小吃',
        '聚餐',
        '做饭材料',
    ],
    '女朋友': [
        '吃饭',
        '游玩',
        '酒店',
        '饮料',
        '礼物',
        '外卖'
    ],
    '购物': [
        '衣服',
        '鞋子',
        '电子产品',
        '超市',
        '京东',
        '淘宝',
        '美团',
        '拼多多'
    ],
    '交通': [
        '地铁',
        '公交',
        '共享单车',
        '共享汽车',
        '打车',
        '火车',
        '飞机',
        '客车'
    ],
    '学习': [
        '买书',
        '文具',
        '其他'
    ],
    '娱乐': [
        '游戏付费',
        'App会员',
        '演唱会',
        '游玩',
        '其他'
    ],
    '生活': [
        '酒店',
        '理发',
        '天然气/电费',
        '房租',
        '看病吃药',
        '其他'
    ],
    '通讯': [
        '电话费',
        '网费'
    ],
    '第三方平台': [
        '花呗',
        '借呗',
        '信用卡'
    ],
    '家人/朋友': [
        '红包',
        '借还款',
    ]
}