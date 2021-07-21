# coding:utf-8
from flask import Blueprint, session, flash, redirect, url_for, request, g

from bluelog.modules.user_github import GithubUser
from bluelog.utils.extensions import github, db
import requests
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
    user = GithubUser.query.filter_by(username=username).first()
    if user is None:
        user = GithubUser(username=username, access_token=access_token)
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



