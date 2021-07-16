# coding:utf-8
from flask import Blueprint, render_template,redirect,url_for

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/', methods=['GET'])
@admin_bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


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


@admin_bp.route('/test', methods=['GET'])
def test():
    return render_template('blog.html')


@admin_bp.route('/favourite', methods=['GET'])
def favourite():
    return render_template('favourite.html')


@admin_bp.route('/update_pwd', methods=['GET'])
def update_pwd():
    return render_template('register.html')


@admin_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@admin_bp.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('admin.login'))


@admin_bp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')


@admin_bp.route('/mailbox', methods=['GET'])
def mailbox():
    return render_template('mailbox.html')


@admin_bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contacts.html')


@admin_bp.route('/package', methods=['GET'])
def package():
    return render_template('package.html')


@admin_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')