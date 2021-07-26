# coding:utf-8
import csv
import json


def read_csv(filename):
    """
    输入文件，返回json的格式
    :param filename:
    :return:
    """
    tableData = []
    with open(filename,'r') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            # 读取的内容是字典格式的
            tableData.append(dict(row))

        return json.dumps(tableData, sort_keys=True, indent=2, ensure_ascii=False)

