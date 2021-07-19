import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)

path_of_current_dir = os.path.split(path_of_current_file)[0]

chdir = path_of_current_dir


workers = 3  # 进程数量
threads = 2 # 线程数量

worker_class = 'sync'

bind='127.0.0.1:5001'  # 监听内网端口5001

pidfile = '%s/gunicorn.pid' % path_of_current_dir  # 存放Gunicorn进程pid的位置，便于跟踪

accesslog = '%s/log/00_gunicorn_access.log' % path_of_current_dir  # 存放访问日志的位置，注意首先需要存在logs文件夹，Gunicorn才可自动创建log文件

errorlog = '%s/log/00_gunicorn_access.log' % path_of_current_dir  # 存放错误日志的位置，可与访问日志相同

reload = True  # 如果应用的代码有变动，work将会自动重启，适用于开发阶段

daemon = True # 是否后台运行

debug = False

timeout = 30   # server端的请求超时秒数

loglevel = 'error'

