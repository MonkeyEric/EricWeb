import os

import click
from bluelog.modules.blog import Admin, Category
from bluelog.modules.user_github import GithubUser

from bluelog.blueprints.user import user_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.blueprints.user_github import github_bp
from flask import Flask, render_template, g

from bluelog.utils.extensions import bootstrap, db, ckeditor, mail, moment, github, login_manager, csrf
from bluelog.settings import config

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('blue_log')
    app.config.from_object(config[config_name])
    app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'file')
    app.config.update(
        GITHUB_CLIENT_ID=os.getenv('GITHUB_CLIENT_ID'),
        GITHUB_CLIENT_SECRET=os.getenv('GITHUB_CLIENT_SECRET'),
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        # 默认标题
        MAIL_DEFAULT_SENDER=('Eric', os.getenv('MAIL_USERNAME'))
    )

    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_commands(app)  # 注册自定义shell命令
    register_errors(app)  # 注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    register_template_context(app)  # 注册模板上下文处理函数
    register_user_info_(app)
    return app


def register_logging(app):
    pass


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(github_bp, url_prefix='/github')


def register_extensions(app):
    github.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_user_info_(app):
    @app.context_processor
    def user_foo():
        is_login = False
        avatar = ''
        username = '访客用户'
        # url = ''
        role = '非用户访问'
        if g.get('user'):
            if g.db == 'github_user':
                is_login = True
                response = github.get('user')
                avatar = response['avatar_url']
                username = response['name']
                # url = response['html_url']
                role = '管理员'
            if g.db == 'admin':
                is_login = True
                user = g.user
                username = user.name
                role = '一级管理员'
        user_info = dict(is_login=is_login, avatar=avatar, username=username, role=role)
        print('username_____', username)
        return dict(user_info=user_info)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', description=e.description), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html', description=e.description), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories,default is 10.')
    @click.option('--post', default=50, help='Quantity of posts,default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments,default is 500.')
    def forge(category, post, comment):
        """generate the fake categories,posts,comments"""
        from bluelog.utils.fakes import fake_admin, fake_categories, fake_posts, fake_comments
        db.drop_all()
        db.create_all()
        click.echo('Generating the administrator……')
        fake_admin()

        click.echo('Generating %d categories……' % category)
        fake_categories(category)

        click.echo('Generating %d posts……' % post)
        fake_posts(post)

        click.echo('Generating %d comments……' % comment)
        fake_comments(comment)

        click.echo('Done.')

    # 命令函数
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def init_db(drop):
        """Initialize the database."""
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')
