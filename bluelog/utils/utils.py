# coding:utf-8
# 辅助函数
from functools import wraps
from flask import request, session, render_template, current_app, redirect, url_for
from flask_mail import Message, Mail

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin


def require_login(func):
    @wraps(func)
    def logic_func(**kwargs):
        if session.get('usercache'):
            return render_template('login.html')

    return logic_func


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
