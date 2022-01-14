# coding:utf-8
# 博客
from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, session, g
from flask_login import login_required
from bluelog.modules.blog import *
from bluelog.utils.forms import AdminCommentFrom, CommentForm
from bluelog.modules.user_github import GithubUser
from flask_login import current_user
from sqlalchemy import desc

import os
import json
import re
import uuid

blog_bp = Blueprint('blog', __name__)


@blog_bp.before_request
def before_request():
    g.user = None
    g.db = None
    if 'user_id' in session:
        g.user = GithubUser.query.get(session['user_id'])
        g.db = 'github_user'
    if current_user.is_authenticated:
        if not g.user:
            g.user = Admin.query.get(current_user.id)
            g.db = 'admin'


@blog_bp.route('/', methods=['GET', 'POST'])
@login_required
def blog_index():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 30
        pagination = Post.query.order_by(desc(Post.timestamp)).paginate(page, per_page=per_page)
        posts = pagination.items

        return render_template('blog_list.html', pagination=pagination, posts=posts)
    if request.method == 'POST' and g.user:
        response = json.loads(request.data.decode('utf-8'))
        post_id = int(response.get('post_id')) if response.get('post_id') else 0
        post = db.session.query(Post).filter_by(id=post_id).first()
        if not post:
            post = Post()
        post.title = response.get('title', '默认题目'+str(datetime.now()))
        post.body_html = response.get('body_html')
        post.body_text = re.sub('<[^<]+?>', '', response.get('body_html','')).replace('\n', '').strip()
        post.body_md = response.get('body_md')
        post.category_id = response.get('category_id', '')
        db.session.add(post)
        db.session.commit()
        if post_id == 0:
            post_id = post.id
        for oid in response.get('label_id', []):
            tag_post = TagPost()
            tag_post.tag_id = oid
            tag_post.post_id = post_id
            db.session.add(tag_post)

        db.session.commit()
        return {'code': '100000', 'msg': '博客上传成功'}


@blog_bp.route('/category/<int:category_id>', methods=['GET'])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(desc(Post.timestamp)).paginate(page, per_page)
    posts = pagination.items

    return render_template('blog.html', pagination=pagination, posts=posts)


@blog_bp.route('/category', methods=['POST'])
def add_category():
    if request.method == 'POST' and g.user and g.user.role == 1:
        print(request.form)
        category = db.session.query(Category).filter_by(name=request.form.get('name')).first()
        if not category:
            c = Category()
            c.name = request.form.get('name')
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('admin.index'))
        else:
            return {'code': '100111', 'msg': '名字已经有，请重新填写'}
    return {'code': '100111', 'msg': '操作失败'}


@blog_bp.route('/tag/<int:tag_id>', methods=['GET'])
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('blog.html',  posts=posts)


@blog_bp.route('/tag', methods=['POST'])
def add_tag():
    if request.method == 'POST' and g.user:
        tag = db.session.query(Tag).filter_by(name=request.form.get('name')).first()
        if not tag:
            t = Tag()
            t.name = request.form.get('name')
            db.session.add(t)
            db.session.commit()
            return redirect(url_for('admin.index'))
        else:
            return {'code': '100111', 'msg': '名字已经有，请重新填写'}
    return {'code': '100111', 'msg': '操作失败'}


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    """
    发表评论
    """
    tag_list = []
    tag = db.session.query(TagPost,Tag).filter(TagPost.tag_id==Tag.id).filter(TagPost.post_id==post_id).all()
    # tag = TagPost.query.join(Tag,TagPost.tag_id==Tag.id).filter(TagPost.post_id==post_id).all()

    for oid in tag:
        tag_list.append({'tag_id':oid[1].id,'name':oid[1].name})
    post = Post.query.get_or_404(post_id)
    if not post.read_count:
        read_count = 0
    else:
        read_count = post.read_count
    db.session.query(Post).filter_by(id=post_id).update({"read_count": read_count+1})
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(desc(Comment.timestamp)).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentFrom()
        form.author.data = current_user.name
        form.email.data = current_app.config['WEB_EMAIL']
        form.site.data = url_for('blog.blog_index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = True
        reviewed = True
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body, from_admin=from_admin, post=post, reviewed=reviewed
        )
        replied_id = request.args.get('reply')

        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            # 发送邮件
            pass
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论已发表', 'success')
        else:
            flash('非常感谢,你的评论经过审核将会发表', 'info')
            # 发送邮件
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('article.html', post=post, pagination=pagination, form=form, comments=comments, tag_list=tag_list)


@blog_bp.route('/post', methods=['PUT'])
def put_post_():
    receive = request.json
    post_id = int(receive.get('post_id'))
    if receive.get('status') == 'read':
        read_count = int(receive.get('read_count', 0))
        db.session.query(Post).filter_by(id=post_id).update({"read_count": read_count})
        db.session.commit()
        return {"code": "100000", "mgs": "ok"}
    elif receive.get('status') == 'like':
        like_count = int(receive.get('like_count', 0))
        db.session.query(Post).filter_by(id=post_id).update({"like_count": like_count})
        db.session.commit()
        return {"code": "100000", "mgs": "ok"}
    else:
        return {"code": "100011", "mgs": "status参数错误"}


@blog_bp.route('/master', methods=['GET'])
def master():
    return render_template('forum_main.html')


@blog_bp.route('/github', methods=['POST'])
def github():
    return render_template('package.html')


@blog_bp.route('/code_editor', methods=['GET'])
def code_editor():
    post_id = request.args.get('post_id', '')
    tag_list = []
    title = ''
    if post_id:
        post = db.session.query(Post).filter_by(id=post_id).first()
        post_md = post.body_md
        category_id = post.category_id
        title = post.title

        tag = db.session.query(TagPost).filter_by(post_id=post_id).all()
        for oid in tag:
            tag_list.append(str(oid.tag_id))
    else:
        post_md = ''
        category_id = ''
    return render_template('form_markdown.html', body=post_md, category_id=category_id, tag_list=tag_list, title=title, post_id=post_id)


@blog_bp.route('/upload', methods=['POST'])
@login_required
def img_upload():
    guid = request.args.get('guid')
    img_data = request.files.get('editormd-image-file')
    if not guid:
        return {"success": 0, "message": "上传失败"}
    file_path = os.path.join(current_app.config['IMG_PATH'], guid + img_data.filename)
    img_data.save(file_path)
    url = '/static/file/img/' + guid + img_data.filename
    return {"success": 1, "message": "上传成功", "url": url}
