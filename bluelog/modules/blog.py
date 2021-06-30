#coding:utf-8
# 存放项目的模型
from datetime import datetime

# 导入SQLAlchemy模块
from bluelog.extensions import db
#from mongoengine import *
# 初始化db
db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    a_create_time = db.Column(db.DateTime, default=datetime.now)
    

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    posts = db.relationship('Post',back_populates='category')



class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer,db.ForeginKey('category.id'))
    category = db.relationship('Category',back_populates='posts')

    comments = db.relationship('Comment',backref='post',cascade='all')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean,default=False)
    reviewed = db.Column(db.Boolean,default=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)

    post_id = db.Column(db.Integer,db.Foreginkey('post.id'))
    post = db.relationship('Post',back_populates='comments')

    replied_id = db.Column(db.Integer,db.Foreginkey('comment.id'))
    relied = db.relationship('Comment',back_populates='replies',remote_side=[id])

    replies = db.relationship('Comment',back_populates='replied',cascade='all')




