# coding:utf-8
from flask import Blueprint, render_template

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
