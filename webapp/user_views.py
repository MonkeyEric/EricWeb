#coding:utf-8
from flask import Flask
from . import user_blueprint
#from ..utils.ch_login import *

@user_blueprint.route('/create_db/')
def ceate_db():
    """创建数据"""
    db.create_all()

@user_blueprint.route('/drop_db/')
def drop_db():
    """删除数据库"""
    db.drop_all()
    return '删除成功'
@user_blueprint.route('/',methods=['GET'])
@user_blueprint.route('/home/',methods=['GET'])
#@is_login
def home():
    """首页"""
    if request.method == 'GET':
        return render_template('index.html')

@user_blueprint.route('/head/',methods=['GET'])
#@is_login
def head():
    """页头"""
    if request.method == 'GET':
        user = session.get('username')
        return render_template('head.html',user=user)

@user_blueprint.route('/left/',methods=['GET'])
def left():
    """左侧栏"""
    if request.method =='GET':
        # 获取登录的用户信息
        user = session.get('username')
        # 获取用户的权限
        permissions = Use.query.filter_by(username=user).first().role.permission
        return render_template('left.html',permission=permissions)



@user_blueprint.route('/register',methods=['GET','POST'])
def register():
    """用户注册界面"""
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        #　获取用户填写的信息
        username = request.form.get('username')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')

        # 定义个变量来控制过滤用户填写的信息
        flag = True
        #　判断用户是否信息都填写了，(all()函数可以判断用户填写的字段是否有空)
        if not all([username,pwd1,pwd2]):
            msg, flag = '* 请填写完整信息',False

        # 判断用户名的长度是否大于16
        if len(username) >16:
            msg,flag = '* 用户名太长',False

        # 判断两次填写的密码是否一致
        if pwd1!= pwd2:
            msg,flag = '* 两次密码不一致',False

        # 如果上面的检查有任一项没有通过就返回注册页面，并提示响应的信息
        if not flag:
            return render_template('register.html',msg=msg)

        #　核对输入的用户是否已经被注册了
        u = User.query.filter(User.username ==username).first()

        # 判断用户是否已经存在
        if u:
            msg = '用户名已经存在'
            return render_template('register.html',msg=msg)

        # 上面的验证全部通过后就开始创建新用户
        user = User(username=username,password=pwd1)
        #　保存注册的用户
        user.save()
        # 跳转到登录页面
        return redirect(url_for('user.login'))

@user_blueprint.route('/login/',methods=['GET','POST'])
def login():
    """登录"""
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #　判断用户名和密码是否填写
        if not all([username,password]):
            msg ='* 请填写好完整的信息'
            return render_template('login.html',msg=msg)

        # 核对用户名和密码是否一致
        if user:
            # 向session中写入相应的数据
            session['user_id'] = user.u_id
            session['username'] = user.username
            return render_template('index.html')

        # 如果用户名和密码不一致返回登录界面，并给提示信息
        else:
            msg = '* 用户名或者密码不一致'
            return render_template('login.html',msg=msg)

@user_blueprint.route('/loginout/',methods=['GET'])
def logout():
    '''退出登录'''
    if request.method == 'GET':
        # 清空session
        session.clear()
        # 跳转到登录页面
        return rendirect(url_for('user.login'))


@user_blueprint.route('/article/',methods=['GET'])
#@is_login
def article_list():
    pass

@user_blueprint.route('/article',methods=['POST'])
#@is_login
def add_article():
    pass


@user_blueprint.route('/changepwd',methods=['GET','POST'])
#@is_login
def change_password():
    if request.method == 'GET':
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        return render_template('changepwd.html',user=user)

    if reqeust.method =='POST':
        username = session.get('username')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        pwd3 = request.form.get('pwd3')

        pwd = User.query.filter(User.password ==pwd1,User.username==username).first()
        if not pwd:
            msg = '请输入正确的旧密码'
            username = session.get('username')
            user = User.query.filter_by(username=username).first()
            return render_template('changepwd.html',msg=msg,user=user)

        else:
            if not all([pwd2,pwd3]):
                msg = '密码不能为空'
                username = session.get('username')
                user = User.query.filter_by(username=username).first()
                return render_template('changepwd.html',msg=msg,user=user)
            if pwd2 != pwd3:
                msg = '两次密码不一致，请重新输入'
                username = session.get('username')
                user = User.query.filter_by(username=username).first()
                return render_template('changepwd.html',msg=msg,user=user)

            pwd.password = pwd2
            db.session.commit()

            return redirect(url_for('user.change_pass_success'))

@user_blueprint.route('/changepwdsu/',methods=['GET'])
#@is_login
def change_pass_success():
    """密码修改成功后"""
    if request.method == 'GET':
        return render_template('changepwdsu.html')


if __name__ == "__main__":
    pass

