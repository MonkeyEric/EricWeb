# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, ValidationError, HiddenField, BooleanField, PasswordField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(1,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SettingForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,30)])
    blog_title = StringField('Blog Title',validators=[DataRequired(),Length(1,60)])
    blog_sub_title = StringField('Blog Sub Title',validators=[DataRequired(),Length(1,100)])
    about = StringField('About Page',validators=[DataRequired()])
    submit = SubmitField()

