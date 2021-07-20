# coding:utf-8
from flask import Blueprint, session, flash, redirect, url_for, request, g
from flask_login import login_required

from bluelog.modules.user_github import *
from bluelog.utils.extensions import github
github_bp = Blueprint('g_user', __name__, template_folder='templates')


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.access_token


@github_bp.route('/auth')
@github.authorized_handler
def authorized(access_token):
    if access_token is None:
        flash('Login failed')
        return redirect(url_for('user.login'))
    response = github.get('user', access_token=access_token)
    username = response['login']  # get username
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username, access_token=access_token)
        db.session.add(user)
    user.access_token = access_token  # update access token
    db.session.commit()
    flash('Login success.')
    # log the user in
    # if you use flask-login, just call login_user() here.
    session['user_id'] = user.id
    return redirect(url_for('admin.index'))


@github_bp.route('/star/helloflask')
def star():
    github.put('user/starred/greyli/helloflask', headers={'Content-Length': '0'})
    flash('Star success.')
    return redirect(url_for('admin.index'))


# 登入
@github_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = '1649107451@qq.com'
        user = User.query.filter_by(email=email).first()

        if user is not None:
            if user.password_hash is None:
                flash('Please use the third patry service to log in.')
                return redirect(url_for('user.login'))
    elif request.method == 'GET':
        if session.get('user_id', None) is None:
            return github.authorize(scope='repo')  # 进行OAuth授权流程
        flash('Already logged in.')
        return redirect(url_for('admin.index'))


# 登出
@github_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Goodbye.')
    return redirect(url_for('user.login'))