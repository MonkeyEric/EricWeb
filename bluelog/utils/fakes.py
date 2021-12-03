# coding:utf-8
from bluelog.modules.blog import Admin, Category, Post, Comment
from bluelog.utils.extensions import db
from faker import Faker
import random


# 用于生成虚拟管理员信息的fake_admin()
def fake_admin():
    admin = Admin(
        email='1649107451@qq.com',
        my_title='Bluelog',
        name='Mima Kirigoe',
        about='Um,l,Mima Kirigoe,had a fun time as a member of CHAM……',
        role=1,
    )
    admin.set_password('123456')
    db.session.add(admin)
    db.session.commit(),


# 用于生成虚拟分类的fake_categories()函数
fake = Faker()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except InterruptedError:
            db.session.rollback()


# 用于生成虚拟文章数据的fake_posts()
def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body_html=fake.text(2000),
            body_md=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


# 用于生成虚拟评论的fake_comments()函数代码
def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    # 管理员发表的评论
    comment = Comment(
        author='Mima Kirigoe',
        email='miam@example.com',
        site='example.com',
        body=fake.sentence(),
        timestamp=fake.date_time_this_year(),
        from_admin=True,
        reviewed=True,
        post=Post.query.get(random.randint(1, Post.query.count()))
    )
    db.session.add(comment)

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
