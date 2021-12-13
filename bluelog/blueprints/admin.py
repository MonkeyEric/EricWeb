# coding:utf-8

from flask import Blueprint, render_template, g, session, send_from_directory, request, current_app, redirect, url_for
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

from bluelog.modules.user_github import GithubUser
from bluelog.modules.blog import *
from bluelog.modules.income_expense import Income
from bluelog.utils.forms import IncomeExpenseForm, FavoriteForm
from bluelog.utils.csv_tools import read_csv, save_to_db
from bluelog.money_excel_model import *
from bluelog.utils.extensions import socketio
from flask_socketio import emit

from datetime import date, time, timedelta, datetime
from sqlalchemy import DateTime, Date, Time, func, desc, extract, asc
import json
import os

admin_bp = Blueprint('admin', __name__)


def find_datetime(value):
    for v in value:
        if isinstance(value[v], datetime):
            value[v] = convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改


def convert_datetime(value):
    if value:
        if isinstance(value, (datetime, DateTime)):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, (date, Date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (Time, time)):
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
        if not g.user:
            g.user = Admin.query.get(current_user.id)
            g.db = 'admin'


@admin_bp.route('/', methods=['GET'])
@admin_bp.route('/index', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(desc(Post.timestamp)).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)


def arrange(res, li_len=13):
    new_consume = {}
    for i in res:
        if not new_consume.get(i[2]):
            new_consume[i[2]] = {}
        new_consume[i[2]][i[1]] = i[0]
    for key, value in new_consume.items():
        new_consume[key] = [round(value.get(i, 0), 2) for i in range(1, li_len)]
    return new_consume


@admin_bp.route('/chart', methods=['GET'])
def chart():
    # 存储
    storage = db.session.query(func.sum(Income.amount)).scalar()
    if '-' in str(storage):
        storage = round(float(str(storage)[1:]), 2)
    # 上个月支出
    now = datetime.now()
    last_month = now.replace(month=now.month - 1)
    expand = db.session.query(func.sum(Income.money)).filter(Income.income_expense == "支出",
                                                             Income.deal_date >= last_month,
                                                             Income.deal_date < now).scalar()
    if '-' in str(expand):
        expand = round(float(expand[1:]), 2)

    # 近一个月支出最高得类型
    high_money_count_type_s = Income.query.filter(Income.deal_date >= now - timedelta(days=30)).order_by(
        desc(Income.money)).first()
    if high_money_count_type_s:
        high_money = {'count_type_s': high_money_count_type_s.count_type_s, 'money': high_money_count_type_s.money}
    else:
        high_money = {'count_type_s': '', 'money': ''}
    # 近一个月支出次数最高得类型
    order_by_type_s = func.count('*').label('total')
    high_count = db.session.query(Income.count_type_s, func.count('*').label('total')).group_by(
        Income.count_type_s).order_by(desc(order_by_type_s)).first()

    # 收入支出比
    res2 = db.session.query(func.sum(Income.money).label('total_money'),
                            extract('month', Income.deal_date).label('month'), Income.income_expense).filter(
        Income.deal_date >= datetime.today().replace(month=1, day=1), Income.income_expense != '',
        Income.income_expense != '/').group_by(
        Income.income_expense, extract('month', Income.deal_date).label('month')).order_by(asc(Income.deal_date))
    income_rate = arrange(res2)
    if income_rate.get('收入', '') and income_rate.get('支出', ''):
        income_rate['存储'] = [round(income_rate['收入'][i] - income_rate['支出'][i], 2) for i in
                             range(len(income_rate['支出']))]
    del res2
    return render_template('graph_chartjs.html', storage=storage, expand=expand, high_money=high_money,
                           high_count=high_count, income_rate=json.dumps(income_rate))


@admin_bp.route('/chart_type', methods=['GET'])
def chart_type():
    res = db.session.query(Income.count_type_f, func.sum(Income.money).label('total_money'),
                           extract('month', Income.deal_date).label('month'),
                           extract('year', Income.deal_date).label('year')).filter(
        Income.income_expense == '支出').group_by(Income.count_type_f).order_by(asc(Income.deal_date))
    consume_type = {}
    for i in res:
        if not consume_type.get(i[1]):
            consume_type[i[0]] = {}

        if not consume_type[i[0]].get(i[3]):
            consume_type[i[0]][i[3]] = {}
        consume_type[i[0]][i[3]][i[2]] = i[1]

    for key, value in consume_type.items():
        for j in range(2018, 2024):
            if not value.get(j):
                value[j] = {}
            value[j] = [round(value[j].get(i, 0), 2) for i in range(1, 13)]
    del res
    # top5类型
    res1 = db.session.query(func.sum(Income.money).label('total_money'),
                            extract('month', Income.deal_date).label('month'), Income.count_type_f).filter(
        Income.income_expense == '支出', Income.deal_date >= datetime.today().replace(
            month=1, day=1)).group_by(
        extract('month', Income.deal_date).label('month')).order_by(asc(Income.deal_date))
    top5_type = arrange(res1, 8)
    del res1
    # top5次数
    res2 = db.session.query(func.count(Income.money).label('total_money'), Income.count_type_f).filter(
        Income.income_expense == '支出', Income.count_type_f != '',
        Income.deal_date >= datetime.today().replace(month=1, day=1)).group_by(Income.count_type_f).order_by(
        desc(Income.count_type_f))
    top5_count = [{'value': i[0], 'name': i[1]} for i in res2]

    # 消费总计
    res = db.session.query(func.sum(Income.money).label('total_money'),
                           extract('month', Income.deal_date).label('month'),
                           extract('year', Income.deal_date).label('year')
                           ).filter(Income.income_expense == '支出').group_by(
        extract('month', Income.deal_date).label('month')).order_by(asc(Income.deal_date))

    consume = arrange(res)
    del res
    res1 = db.session.query(func.count(Income.money).label('total_money'),
                            extract('month', Income.deal_date).label('month'),
                            extract('year', Income.deal_date).label('year')).filter(
        Income.income_expense == '支出').group_by(extract('month', Income.deal_date).label('month')).order_by(
        asc(Income.deal_date))
    consume_count = arrange(res1)

    del res1

    return {'top5_type': top5_type, 'consume_type': consume_type, 'top5_count': top5_count, 'consume': consume,
            'consume_count': consume_count}


@admin_bp.route('/data', methods=['GET', 'POST'])
def table_data():
    son = []
    for key, value in expense_type.items():
        son.append('——%s——' % key)
        for j in value:
            son.append(j)
    return render_template('table.html', fathers=list(expense_type.keys()), sons=son, table='/table')


@admin_bp.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)
        son = request.args.get('son', '')
        father = request.args.get('father', '')
        c_type = request.args.get('type', '')
        re_dict = {}
        if son:
            re_dict['count_type_s'] = son
        if father:
            re_dict['count_type_f'] = father
        if c_type:
            re_dict['income_expense'] = c_type
        if re_dict:
            pagination = Income.query.filter_by(**re_dict).order_by(
                desc(Income.deal_date)).with_entities(Income.deal_date,
                                                      Income.income_expense,
                                                      Income.amount, Income.deal_number,
                                                      Income.count_type_f,
                                                      Income.count_type_s,
                                                      Income.pay_status,
                                                      Income.counterparty,
                                                      Income.goods).paginate(page,
                                                                             per_page=per_page)
        else:
            pagination = Income.query.order_by(desc(Income.deal_date)).with_entities(Income.deal_date,
                                                                                     Income.income_expense,
                                                                                     Income.amount, Income.deal_number,
                                                                                     Income.count_type_f,
                                                                                     Income.count_type_s,
                                                                                     Income.pay_status,
                                                                                     Income.counterparty,
                                                                                     Income.goods).paginate(
                page, per_page=per_page)
        income_result = [dict(zip(r.keys(), r)) for r in pagination.items]
        for r in income_result:
            find_datetime(r)
        return json.dumps({'data': income_result, 'total': pagination.total, 'pages': pagination.pages})
    elif request.method == 'POST':
        response = json.loads(request.data.decode('utf-8'))
        deal_number = response['deal_number']
        response.pop('deal_number')
        Income.query.filter_by(deal_number=deal_number).update(response)
        db.session.commit()
        return json.dumps({'code': 10000, 'msg': 'ok'})


@admin_bp.route('/upload', methods=['GET', 'POST'], strict_slashes=False)
def upload():
    form = IncomeExpenseForm(CombinedMultiDict([request.form, request.files]))
    if request.method == 'POST':
        csv_file = form.file_csv.data
        desc_ = form.desc.data
        filename = secure_filename(csv_file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
        csv_file.save(file_path)
        data_json = read_csv(file_path, desc_)
        owner_id = session.get('_user_id')
        save_to_db(data_json, owner_id)
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


@admin_bp.route('/favourite', methods=['GET', 'POST'])
def favourite():
    # GET的形式，返回相应的html，并且传递相应的form表单CSRF
    form_fav = FavoriteForm(CombinedMultiDict([request.form, request.files]))
    res = Favorite.query.all()
    new_dict = {}
    for i in res:

        if not new_dict.get(i.category):
            new_dict[i.category] = []
        new_dict[i.category].append(
            {'category': i.category, 'name': i.name,
             'avatar': i.avatar, 'web_url': i.web_url,
             'express': i.express,
             'thumb_down': i.thumb_down, 'thumb_up': i.thumb_up})

    if form_fav.validate_on_submit():
        icon = form_fav.icon.data
        filename = secure_filename(icon.filename)
        avatar = os.path.join(current_app.config['fav_img'], filename)
        file_path = os.path.join(current_app.root_path, avatar)
        icon.save(file_path)

        fav = Favorite(name=form_fav.name.data, avatar=avatar, web_url=form_fav.web_url.data,
                       express=form_fav.express.data,
                       thumb_up=0, thumb_down=0, category=form_fav.category.data)
        db.session.add(fav)
        db.session.commit()

    # POST的形式，进行添加相应的网站，
    return render_template('favourite.html', form=form_fav, data_fav=new_dict)


@admin_bp.route('/img', methods=['POST'])
def img_save():
    return render_template('profile.html')


@admin_bp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')


@admin_bp.route('/package', methods=['GET'])
def package():
    return render_template('package.html')


@admin_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@admin_bp.route('/file_manage', methods=['GET'])
def file_manage():
    return render_template('file_manager.html')
