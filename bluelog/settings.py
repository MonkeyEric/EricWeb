# coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(basedir)


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('EricWeb Admin',MAIL_USERNAME)

    ERICWEB_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'mysql:///'+os.path.join(basedir, 'data-dev.db')
    DEBUG=True
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root001@192.168.40.52/develop'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Zjq;;123456@localhost/develop'



class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Wh;;1314@127.0.0.1/test?charset=utf8'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Wh;;1314@127.0.0.1/product?charset=utf8'


config = {
        'development':DevelopmentConfig,
        'testing':TestingConfig,
        'production':ProductionConfig
        }

