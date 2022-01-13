# coding:utf-8
import re
import base64
import json
import requests as req
from PIL import Image
from io import BytesIO


def get_keyword_desc(url):
    response = req.get(url)
    result = response.text
    data = {}
    try:
        title = re.compile(r"<title>(.*?)</title>").findall(result)
        keyword = re.compile(r'<meta name="keywords" content="(.*?)"').findall(result)
        desc = re.compile(r'<meta name="description" content="(.*?)"').findall(result)
        if not title or not keyword or not desc:
            data.update({"url": url})
            return {"code": "100111", "msg": "ok", "data": data}
        data.update({"title": title, "keyword": keyword, "desc": desc})
        return {"code": "100000", "msg": "ok", "data": data}
    except:
        data.update({"url": url})
        return {"code": "100111", "msg": "ok", "data": data}


def get_web_icon(url):
    response = req.get(url + "/favicon.ico")

    # 内存中打开图片
    image = Image.open(BytesIO(response.content))

    # 图片的base64编码
    ls_f = base64.b64encode(BytesIO(response.content).read())

    # base64编码解码
    imgdata = base64.b64decode(ls_f)

    # 图片文件保存
    filename = '.'.join(url.split('.')[1:]) + '.ico'
    with open(filename, 'wb') as f:
        f.write(imgdata)


def save_database(data, category):
    # 搭建rabbit mq将任务存储到消息队列中，爬虫的脚本一直监控
    pass


def main(url_list, category):
    for url in url_list:
        res = get_keyword_desc(url)
        if res.get('code') != "100000":
            item_list = []
            item_list.append(res['data'].get("url"))
            with open("favorite_web_error.json", "r") as f:
                load_dict = json.load(f)
                for i in range(len(load_dict)):
                    item_list.append(load_dict[i])
            if item_list:
                with open("favorite_web_error.json", "w") as f1:
                    json.dump(item_list, f1)
        save_database(res, category)


if __name__ == '__main__':
    main()
