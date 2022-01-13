# coding:utf-8
# 辅助函数
import os
from functools import wraps
from flask import request, session, render_template, current_app, redirect, url_for
from flask_mail import Message, Mail
from random import Random
from jobs import *



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




