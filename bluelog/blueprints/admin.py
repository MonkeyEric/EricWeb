# coding:utf-8
from flask import Blueprint, render_template, g, session, send_from_directory, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

from bluelog.modules.user_github import GithubUser
from bluelog.modules.blog import *
from bluelog.modules.income_expense import Income
from bluelog.utils.forms import IncomeExpenseForm, IncomeForm
from bluelog.utils.csv_tools import read_csv, save_to_db
from bluelog import config_dict

from datetime import datetime as cdatetime
from datetime import date, time, timedelta
from sqlalchemy import DateTime, Numeric, Date, Time, func
import json
import os

admin_bp = Blueprint('admin', __name__)


def find_datetime(value):
    for v in value:
        if (isinstance(value[v], cdatetime)):
            value[v] = convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改


def convert_datetime(value):
    if value:
        if (isinstance(value, (cdatetime, DateTime))):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif (isinstance(value, (date, Date))):
            return value.strftime("%Y-%m-%d")
        elif (isinstance(value, (Time, time))):
            return value.strftime("%H:%M:%S")
    else:
        return ""




@admin_bp.after_request
def after_request(response):
    # 调用函数生成csrf token
    csrf_token = generate_csrf()
    # 设置cookie传给前端
    response.set_cookie('csrf_token', csrf_token)
    return response


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
    print('22222', current_app.root_path)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)


@admin_bp.route('/chart', methods=['GET'])
def chart():
    # 存储
    storage = round(db.session.query(func.sum(Income.amount)).scalar(),2)
    # 上个月支出
    now = cdatetime.now()
    last_month = now.replace(month=now.month-1)
    expand = round(db.session.query(func.sum(Income.money)).filter(Income.income_expense=="支出",Income.deal_date>=last_month,Income.deal_date<now).scalar(),2)
    # 近一个月支出最高得类型
    high_money_count_type_s = Income.query.filter(Income.deal_date>=now-timedelta(days=30)).order_by(Income.money.desc()).first()
    high_money = {'count_type_s':high_money_count_type_s.count_type_s,'money':high_money_count_type_s.money}
    print(high_money_count_type_s)
    # 近一个月支出次数最高得类型
    high_count = db.session.query(func.count(Income.count_type_s)).scalar()
    print(high_count)
    # 消费总计
    # 消费类型总计
    # 收入支出比
    # TOP3消费类型折线图
    # Top5支付次数扇形图

    return render_template('graph_chartjs.html')


@admin_bp.route('/data', methods=['GET', 'POST'])
def table_data():
    form = IncomeForm()

    son = []
    for key,value in config_dict.Expense_type.items():
        son.append('——%s——'%key)
        for j in value:
            son.append(j)
    return render_template('table.html', fathers=list(config_dict.Expense_type.keys()),sons=son)


@admin_bp.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        pagination = Income.query.order_by(Income.deal_date.desc()).with_entities(Income.deal_date,
                                                                                  Income.income_expense,
                                                                                  Income.amount, Income.deal_number,
                                                                                  Income.count_type_f,
                                                                                  Income.count_type_s,
                                                                                  Income.pay_status,
                                                                                  Income.counterparty,
                                                                                  Income.goods).paginate(page,
                                                                                                         per_page=per_page)
        income_result = [dict(zip(r.keys(), r)) for r in pagination.items]
        for r in income_result:
            find_datetime(r)
        return json.dumps({'data': income_result, 'total': pagination.total, 'pages': pagination.pages})
    elif request.method == 'POST':
        response = json.loads(request.data.decode('utf-8'))
        deal_number = response['deal_number']
        response.pop('deal_number')
        res = Income.query.filter_by(deal_number=deal_number).update(response)
        db.session.commit()
        return json.dumps({'code': 10000, 'msg': 'ok'})


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
        return redirect(url_for('admin.table_data'))
    return render_template('form_file_upload.html', form=form)


@admin_bp.route('/download/<string:filetype>', methods=['GET'])
def download(filetype):
    current_dir = os.path.join(current_app.root_path, 'file')
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


@admin_bp.route('/file_manage', methods=['GET'])
def file_manage():
    return render_template('file_manager.html')
