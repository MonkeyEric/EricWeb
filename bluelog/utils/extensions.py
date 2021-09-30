# coding:utf-8
# 扩展
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_github import GitHub
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sockets import Sockets
from flask_socketio import SocketIO

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
github = GitHub()
login_manager = LoginManager()
csrf = CSRFProtect()
sockets = Sockets()
socketio = SocketIO()


@login_manager.user_loader
def load_user(user_id):
    from bluelog.modules.user_github import GithubUser
    from bluelog.modules.blog import Admin
    user = Admin.query.get(int(user_id))
    g_user = GithubUser.query.get(int(user_id))
    if g_user:
        return g_user
    else:
        return user


login_manager.login_view = 'user.login'
login_manager.login_message = '你必须登录后才能访问该页面'
login_manager.login_message_category = 'info'