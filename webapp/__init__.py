# coding:utf-8
from flask import Blueprint

api_blueprint = Blueprint(
        'admin_blueprint',
        __name__,
        url_prefix= '/api'
        )
from . import users, auth
