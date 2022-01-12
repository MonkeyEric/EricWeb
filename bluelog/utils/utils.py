# coding:utf-8
# 辅助函数
import os
from functools import wraps
from flask import request, session, render_template, current_app, redirect, url_for
from flask_mail import Message, Mail
from random import Random

import pika
import json

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def generate_random_code():
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    random = Random()
    x = random.sample(chars, 4)
    return "".join(x)


def cache_login(userdata):
    user_key = lambda x: "eric_web_%s" % x
    key = user_key(userdata.get('id'))

    session['user_cache'] = key
    del userdata['password']
    session.cache = userdata
    # redis.set(key, dumps(userdata, cls=JsonRespEncoder))


class RabbitMqUtils(object):
    def __init__(self, username, password, host, port, queue):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.queue = queue

    def producer(self):
        credentials = pika.PlainCredentials(self.username, self.password)  # mq用户名和密码
        # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, virtual_host='/', credentials=credentials))
        channel = connection.channel()
        # 声明消息队列，消息将在这个队列传递，如不存在，则创建
        result = channel.queue_declare(queue=self.queue, durable=True)

        for i in range(10):
            message = json.dumps({'OrderId': "1000%s" % i})
            # 向队列插入数值 routing_key是队列名
            channel.basic_publish(exchange='', routing_key=self.queue, body=message, properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
            print(message)
        connection.close()

    def consumer(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, virtual_host='/', credentials=credentials))
        channel = connection.channel()
        # 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
        channel.queue_declare(queue=self.queue, durable=True)

        # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
        def callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(body.decode())

        # 告诉rabbitmq，用callback来接收消息
        channel.basic_consume(self.queue, callback)
        # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
        channel.start_consuming()


rm = RabbitMqUtils(username="guest", password="guest", host="localhost", port=5672, queue="fav_web")
# rm.port = 15679        # int(os.getenv("RabbitMqPort"))
# rm.host = "localhost"  # os.getenv("RabbitMqHost")
# rm.password = "guest"  # os.getenv("RabbitMqPassword")
# rm.username = "guest"  # os.getenv("RabbitMqUsername")
