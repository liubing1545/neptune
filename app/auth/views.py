# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    ChangeEmailForm


# 用户登录
# Returns: 返回登录页面；若用户提交登录表单，返回主页；
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        # 如果信息对称则登录用户
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'邮箱或密码不正确')
    return render_template('auth/login.html', form=form)


# 用户登出
# 必要条件：用户需先登录
# Returns: 返回主页
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已登出')
    return redirect(url_for('main.index'))


# 用户注册
# Returns：返回注册页面；若用户提交注册表单，返回主页面；
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 添加用户到数据库
        user = User(
            user_email=form.user_email.data,
            user_name=form.user_name.data,
            user_eid=form.user_eid.data,
            hash_password=form.password.data,
            user_tel=form.user_tel.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


# 用户更改密码
# 必要条件：用户需先登录
# Returns: 返回更改密码页面；若用户提交更改密码表单，返回主页；
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # 检验密码是否正确
        if current_user.verify_password(form.old_password.data):
            current_user.hash_password = form.password.data
            db.session.add(current_user)
            flash(u'密码已更新')
            return redirect(
                url_for('main.user', username=current_user.user_name))
        else:
            flash(u'密码不正确')
    return render_template("auth/change_password.html", form=form)


# 用户更改邮箱
# 必要条件：用户需先登录
# Returns：返回更改邮箱页面；若用户提交有效更改邮箱表单，返回主页；
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.user_email = form.email.data
            db.session.add(current_user)
            flash(u'邮箱已更改')
            return redirect(
                url_for('main.user', username=current_user.user_name))
        else:
            flash(u'邮箱或密码不正确')
    return render_template("auth/change_email.html", form=form)
