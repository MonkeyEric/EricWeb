# coding:utf-8
from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from flask_login import current_user, login_user, logout_user

from bluelog.modules.blog import Admin

from bluelog.utils.emails import send_subscribe_mail
from bluelog.utils.forms import LoginForm, SettingForm
from bluelog.utils.utils import redirect_back, generate_random_code
from bluelog.utils.extensions import github, db
from werkzeug.security import generate_password_hash

from sqlalchemy import or_

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated or session.get('user_id', None) is not None:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        admin = db.session.query(Admin).filter(or_(Admin.email == email, Admin.name == email)).all()
        if len(admin):
            if (email == admin[0].email or email.lower() == admin[0].name) and admin[0].validate_password(password):
                login_user(admin[0], remember)
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


@user_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        subscribe(email)
    return render_template('forgot_password.html', form=form)


@user_bp.route('/update_pwd', methods=['POST', 'GET'])
def update_pwd():
    form = LoginForm()
    return render_template('update_pwd.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SettingForm()
    if request.method == 'POST':
        email = form.email.data
        search_res = db.session.query(Admin).filter(or_(Admin.email == email, Admin.name == email)).all()
        if search_res:
            return render_template('register.html', message='用户已经存在，请重新注册', form=form)
        my_title = form.my_title.data
        name = form.name.data
        role = form.role.data
        about = form.about.data
        password = form.password.data
        admin = Admin(
            email=email,
            my_title=my_title,
            name=name,
            about=about,
            role=role
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('user.login'))
    if request.method == 'GET':
        return render_template('register.html', form=form)


def subscribe(email):
    flash('welcome on board')
    admin = Admin.query.filter_by(email=email).first()
    origin_pwd = generate_random_code()
    Admin.query.filter_by(email=email).update({'password_hash': generate_password_hash(origin_pwd)})
    db.session.commit()
    print(origin_pwd)
    if admin:
        # send_mail('Subscribe Success', email, 'Hello,Thank you for subscribing Flask Weekly!')
        send_subscribe_mail('发送邮件', email, name=admin.name, origin_pwd=origin_pwd)
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('user.forget_password'))
