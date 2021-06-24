# coding:utf-8
from flask import Blueprint
auth_bp = Blueprint('auth',__name__,template_folder='templates')

@auth_bp.route('/login')
def login():
    pass


@auth_bp.route('/logout')
def logout():
    pass

