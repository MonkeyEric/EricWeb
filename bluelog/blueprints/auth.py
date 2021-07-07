# coding:utf-8
from flask import Blueprint, render_template,flash
from flask_login import current_user
#from blog.forms import LoginForm
#from bluelog.models import Admin
#from bluelog.utils import redirect_back

auth_bp = Blueprint('auth',__name__,template_folder='templates')

#@auth_bp.route('/login',methods=['GET','POST'])
#def login():
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


@auth_bp.route('/index')
def index():
    return render_template('index.html')

