# coding:utf-8
# 博客
from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, session, g
from bluelog.modules.blog import *
from bluelog.utils.forms import AdminCommentFrom, CommentForm
from bluelog.modules.user_github import GithubUser
from flask_login import current_user
from sqlalchemy import desc

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


@blog_bp.route('/', methods=['GET'])
def blog_get():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    pagination = Post.query.order_by(desc(Post.timestamp)).paginate(page, per_page=per_page)
    posts = pagination.items

    return render_template('blog_list.html', pagination=pagination, posts=posts)


@blog_bp.route('/category/<int:category_id>', methods=['GET'])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(desc(Post.timestamp)).paginate(page, per_page)
    posts = pagination.items

    return render_template('blog.html', pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(desc(Comment.timestamp)).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentFrom()
        form.author.data = current_user.name
        form.email.data = current_app.config['WEB_EMAIL']
        form.site.data = url_for('blog.blog_get')
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
    return render_template('article.html', post=post, pagination=pagination, form=form, comments=comments)


@blog_bp.route('/master', methods=['GET'])
def master():
    return render_template('forum_main.html')


@blog_bp.route('/github', methods=['POST'])
def github():
    return render_template('package.html')


@blog_bp.route('/code_editor', methods=['GET'])
def code_editor():
    return render_template('form_markdown.html')
