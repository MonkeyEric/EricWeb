# coding:utf-8
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField, ValidationError, HiddenField, BooleanField, PasswordField, \
    DateTimeField, FileField
from wtforms.validators import DataRequired, Length, InputRequired, Email, URL
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SettingForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 40)])
    name = StringField('name', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = StringField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class IncomeExpenseForm(FlaskForm):
    file_csv = FileField(validators=[FileRequired('文件必传'), FileAllowed(['csv'], message='文件格式错误')])
    desc = StringField(validators=[DataRequired()])
    submit = SubmitField()


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[DataRequired(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentFrom(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField()
