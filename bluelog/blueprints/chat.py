# coding:utf-8
from flask import render_template, redirect, url_for, request, Blueprint, current_app, abort
from flask_login import current_user, login_required
from flask_socketio import emit

from bluelog.utils.extensions import socketio, db
from bluelog.utils.forms import ProfileForm
from bluelog.modules.chat_user import Message, User
from bluelog.utils import to_html, flask_errors