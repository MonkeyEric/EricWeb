# coding:utf-8
import pika
import json
import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print('env  path_____',dotenv_path)
load_dotenv(dotenv_path=dotenv_path)


class RabbitMqUtils(object):
    def __init__(self, username=os.getenv("RabbitMqUsername"), password=os.getenv("RabbitMqPassword"), host=os.getenv("RabbitMqHost"), port=int(os.getenv("RabbitMqPort")), queue=os.getenv("RabbitQueue")):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.queue = queue

    def producer(self, data):
        credentials = pika.PlainCredentials(self.username, self.password)  # mq用户名和密码
        # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, virtual_host='/', credentials=credentials))
        channel = connection.channel()
        # 声明消息队列，消息将在这个队列传递，如不存在，则创建
        result = channel.queue_declare(queue=self.queue, durable=True)

        message = json.dumps(data)
        # 向队列插入数值 routing_key是队列名
        channel.basic_publish(exchange='', routing_key=self.queue, body=message, properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
        print(message)
        connection.close()

    def consumer(self, func):
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, virtual_host='/', credentials=credentials))
        channel = connection.channel()
        # 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
        channel.queue_declare(queue=self.queue, durable=True)

        # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
        def callback(ch, method, properties, body):
            print(body.decode())
            func(body.decode())
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # 告诉rabbitmq，用callback来接收消息
        channel.basic_consume(self.queue, callback)
        # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
        channel.start_consuming()


rabbit = RabbitMqUtils()