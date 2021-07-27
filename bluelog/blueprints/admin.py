# coding:utf-8
from flask import Blueprint, render_template, redirect, url_for, g, session, send_from_directory, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

from bluelog.modules.user_github import GithubUser
from bluelog.modules.blog import Admin
from bluelog.utils.forms import IncomeExpenseForm
from bluelog.utils.csv_tools import read_csv, save_to_db

import os, time

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.before_request
def before_request():
    g.user = None
    g.db = None
    if 'user_id' in session:
        g.user = GithubUser.query.get(session['user_id'])
        g.db = 'github_user'
    if current_user.is_authenticated:
        print(current_user)
        if not g.user:
            g.user = Admin.query.get(current_user.id)
            g.db = 'admin'
    print(g.user)


@admin_bp.route('/', methods=['GET'])
@admin_bp.route('/index', methods=['GET'])
# @login_required
def index():
    return render_template('index.html')


@admin_bp.route('/chart', methods=['GET'])
def chart():
    return render_template('graph_chartjs.html')


@admin_bp.route('/data', methods=['GET'])
def table_data():
    return render_template('table_data_tables.html')


@admin_bp.route('/upload', methods=['GET', 'POST'], strict_slashes=False)
def upload():
    form = IncomeExpenseForm(CombinedMultiDict([request.form, request.files]))
    if form.validate_on_submit():
        csv_file = form.file_csv.data
        desc = form.desc.data
        filename = secure_filename(csv_file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
        csv_file.save(file_path)
        data_json = read_csv(file_path, desc)
        save_to_db(data_json)
    return render_template('form_file_upload.html', form=form)





@admin_bp.route('/download/<string:filetype>', methods=['GET'])
def download(filetype):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(current_dir, filetype, as_attachment=True)


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
