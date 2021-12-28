# coding:utf-8
from datetime import datetime,timedelta
breath_date= "2021/06/14"
now = datetime.strptime(breath_date, "%Y/%m/%d")
date = (now + timedelta(days = 50)).strftime("%Y/%m/%d %H:%M:%S")
print(now,date)
