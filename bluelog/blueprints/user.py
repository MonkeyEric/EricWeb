# coding:utf-8
from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user

from bluelog.modules.blog import Admin

from bluelog.utils.emails import send_mail, send_subscribe_mail
from bluelog.utils.forms import LoginForm
from bluelog.utils.utils import redirect_back
from bluelog.utils.extensions import github

user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated or session.get('user_id', None) is not None:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        admin = Admin.query.first()
        if admin:
            print(admin.validate_password(password))
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back,', 'Eric')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)


@user_bp.route('/github/login', methods=['GET'])
def github_login():
    if session.get('user_id', None) is None:
        return github.authorize(scope='repo')  # 进行OAuth授权流程
    flash('Already logged in.')
    return redirect(url_for('admin.index'))


@user_bp.route('/logout')
# @login_required
def logout():
    session.pop('user_id', None)
    # flash('Goodbye.')
    # return redirect(url_for('user.login'))
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('user.login'))


@user_bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contacts.html')


@user_bp.route('/forget_password', methods=['GET'])
def forget_password():
    return render_template('forgot_password.html')


@user_bp.route('/update_pwd', methods=['GET'])
def update_pwd():
    return render_template('register.html')


@user_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@user_bp.route('/subscribe')
def subscribe():
    email = '1649107451@qq.com'
    flash('welcome on board')
    # send_mail('Subscribe Success', email, 'Hello,Thank you for subscribing Flask Weekly!')
    send_subscribe_mail('Subscribe Success', email, name='艾瑞克')
    return redirect(url_for('admin.index'))
