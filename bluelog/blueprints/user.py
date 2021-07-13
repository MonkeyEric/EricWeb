# coding:utf-8
from flask import Blueprint, render_template, flash
from flask_login import current_user

from bluelog.utils.emails import send_mail,send_subscribe_mail
from flask import redirect, url_for

user_bp = Blueprint('user', __name__, template_folder='templates')


# @auth_bp.route('/login',methods=['GET','POST'])
# def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('blog.index'))
#    form = LoginForm()
#    if form.validate_on_submit():
#        username = form.username.data
#        password = form.password.data
#        remember = form.remember.data

#       admin = Admin.query.first()
#        if admin:
#            if username == admin.username and admin.validate_password(password):
#                login_user(admin, remember)
#                flask('Welcome back,','Eric')
#                return redirect_back()
#
#   return render_template('auth/login.html')


@user_bp.route('/subscribe')
def subscribe():
    email = '1649107451@qq.com'
    flash('welcome on board')
    # send_mail('Subscribe Success', email, 'Hello,Thank you for subscribing Flask Weekly!')
    send_subscribe_mail('Subscribe Success', email, name='艾瑞克')
    return redirect(url_for('admin.index'))
