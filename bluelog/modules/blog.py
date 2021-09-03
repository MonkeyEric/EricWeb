# coding:utf-8
# 存放项目的模型
from datetime import datetime

# 导入SQLAlchemy模块
from bluelog.utils.extensions import db
from sqlalchemy_utils import ChoiceType
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    types_choices = (
        (1, '管理员'),
        (2, '一级用户'),
        (3, '二级用户'),
        (4, '三级用户'),
    )
    id = db.Column(db.Integer, primary_key=True)
    role = ChoiceType(types_choices)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    my_title = db.Column(db.String(60))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    a_create_time = db.Column(db.DateTime, default=datetime.now)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))


class Wiki(db.Model):
    # 这个到开发的时候，可以根据情况存储到本地md文件中
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    title = db.Column(db.String(80))
    tag = db.Column(db.String(80))
    body = db.Column(db.Text)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(150))  # 图片地址
    web_url = db.Column(db.String(150))
    name = db.Column(db.String(30))
    express = db.Column(db.String(80))
    thumb_down = db.Column(db.Integer)
    category = db.Column(db.String(30))
    thumb_up = db.Column(db.Integer)
