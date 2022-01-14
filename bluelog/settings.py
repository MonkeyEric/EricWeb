# coding:utf-8
"""
配置文件：
1. 基础配置文件
2. 开发环境
3. 生产环境配置
"""
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('EricWeb Admin', MAIL_USERNAME)

    WEB_EMAIL = os.getenv('BLOG_EMAIL')
    BLOG_POST_PER_PAGE = 5
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15
    TABLE_PER_PAGE = 10

    JSON_AS_ASCII = False


class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'mysql:///'+os.path.join(basedir, 'data-dev.db')
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_PRODUCT_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
