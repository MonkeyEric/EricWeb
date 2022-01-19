# coding:utf-8
import json
import re
import requests
from bs4 import BeautifulSoup
from modues import Favorite

from task import rabbit


def save_to_db(data):
    from modues import session
    f = Favorite()
    f.avatar = data.get('avatar')
    f.web_url = data.get('url')
    f.name = data.get('title')[:30]
    f.express = data.get('desc')[:200]
    f.category = data.get('category')
    session.add(f)
    session.commit()


def get_web_data(url):
    try:
        html = requests.get(url)
        bsObj = BeautifulSoup(html.content, 'html.parser')
    except Exception as e:  # http异常处理
        print(e)
        return {}
    title_ = bsObj.title.string
    description = bsObj.find(attrs={"name": "description"})
    description = description['content'] if description else ''
    keywords = bsObj.find(attrs={"name": "keywords"})
    keywords = keywords['content'] if keywords else ''
    url = url[:-1] if url[-1] =='/' else url
    return {"title": title_, "keywords": keywords, "desc": description, "url": url, "avatar": url+"/favicon.ico"}


def main_fav_webs(receive):
    receive = json.loads(receive)
    category = receive.get('category')
    li = receive.get('task_li')
    for item in li:
        result = get_web_data(item)
        if result:
            result.update({'category':category})
            save_to_db(result)


if __name__ == '__main__':
    rabbit.consumer(main_fav_webs)
