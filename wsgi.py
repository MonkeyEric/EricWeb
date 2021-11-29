# coding:utf-8
"""
启动入口
"""
import os
from dotenv import load_dotenv
from bluelog import create_app
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app()
if __name__ == "__main__":
    app.run("127.0.0.1",5001,debug = True)

