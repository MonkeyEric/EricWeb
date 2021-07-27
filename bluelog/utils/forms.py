# coding:utf-8
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextField, ValidationError, HiddenField, BooleanField, PasswordField, \
    DateTimeField, FileField
from wtforms.validators import DataRequired, Length, InputRequired
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






