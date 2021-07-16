# coding:utf-8
# 辅助函数
from functools import wraps
from flask import session, render_template, current_app
from flask_mail import Message, Mail



def require_login(func):
    @wraps(func)
    def logic_func(**kwargs):
        if session.get('usercache'):
            return render_template('login.html')

    return logic_func


