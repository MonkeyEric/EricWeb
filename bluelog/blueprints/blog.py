# coding:utf-8
# 博客
from flask import Blueprint, render_template

blog_bp = Blueprint('blog', __name__, template_folder='templates')


@blog_bp.route('/', methods=['GET'])
def blog_get():
    return render_template('blog.html')


@blog_bp.route('/master', methods=['GET'])
def master():
    return render_template('forum_main.html')


@blog_bp.route('/github', methods=['POST'])
def github():
    return render_template('package.html')


@blog_bp.route('/code_editor', methods=['GET'])
def code_editor():
    return render_template('form_markdown.html')
