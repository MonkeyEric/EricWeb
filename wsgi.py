# coding:utf-8
"""
启动入口
"""
import os
from dotenv import load_dotenv
from bluelog import create_app
from gevent import pywsgi
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app()
if __name__ == "__main__":
    server = pywsgi.WSGIServer(("127.0.0.1",5001),app)
    server.serve_forever()

