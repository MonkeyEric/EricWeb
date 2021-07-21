# coding:utf-8
from flask import Blueprint, render_template, redirect, url_for, g, session
from flask_login import login_required
from bluelog.utils.extensions import github

from bluelog.modules.user_github import GithubUser
admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = GithubUser.query.get(session['user_id'])


@admin_bp.route('/', methods=['GET'])
@admin_bp.route('/index', methods=['GET'])
# @login_required
def index():
    if g.user:
        is_login = True
        response = github.get('user')
        avatar = response['avatar_url']
        username = response['name']
        url = response['html_url']

        return render_template('index.html', is_login=is_login, avatar=avatar, username=username, url=url)
    is_login = False
    return render_template('index.html', is_login=is_login, username='访客用户')


@admin_bp.route('/chart', methods=['GET'])
def chart():
    return render_template('graph_chartjs.html')


@admin_bp.route('/data', methods=['GET'])
def table_data():
    return render_template('table_data_tables.html')


@admin_bp.route('/upload', methods=['GET'])
def upload():
    return render_template('form_file_upload.html')


@admin_bp.route('/calendar', methods=['GET'])
def calendar():
    return render_template('calendar.html')


@admin_bp.route('/timeline', methods=['GET'])
def timeline():
    return render_template('timeline.html')


@admin_bp.route('/gallery', methods=['GET'])
def gallery():
    return render_template('basic_gallery.html')


@admin_bp.route('/video', methods=['GET'])
def video():
    return render_template('video.html')


@admin_bp.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contacts.html')


@admin_bp.route('/favourite', methods=['GET'])
def favourite():
    return render_template('favourite.html')


@admin_bp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')


@admin_bp.route('/mailbox', methods=['GET'])
def mailbox():
    return render_template('mailbox.html')


@admin_bp.route('/package', methods=['GET'])
def package():
    return render_template('package.html')


@admin_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
