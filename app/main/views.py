# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash,\
    abort
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User
from ..decorators import admin_required


# 显示主页
# 必要条件：用户需先登录
# Returns：返回主页面
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


# 显示用户主页
# 必要条件： 用户需先登录
# Returns：用户个人主页面
@main.route('/home')
@login_required
def home():
    return render_template('home.html')


# 显示用户信息
# 必要条件： 用户需先登录
# Returns：用户个人主信息页面
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        abort(404)
    return render_template('user_info.html', user=user)


# 编辑用户个人信息
# 必要条件： 用户需先登录
# Returns：显示更改用户个人信息页面；若提交更改个人信息表单，则返回用户个人信息页面
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    # 提交更改信息
    if form.validate_on_submit():
        current_user.user_tel = form.tel.data
        db.session.add(current_user)
        flash(u'您的信息已更新')
        return redirect(url_for('.user', username=current_user.user_name))
    # 显示用户信息
    form.tel.data = current_user.user_tel
    return render_template('edit_profile.html', form=form)


# 显示用户主页
# 必要条件： 用户需先登录
#           用户类型需是管理员
# Returns：显示管理员更改用户个人信息页面；若提交管理员更改用户信息表单则返回用
#          户个人信息页面
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    # 提交更改信息
    if form.validate_on_submit():
        user.user_name = form.username.data
        user.user_tel = form.tel.data
        db.session.add(user)
        flash(u'用户信息已被更新')
        return redirect(url_for('.user', username=user.user_name))
    # 显示用户信息
    form.username.data = user.user_name
    form.tel.data = user.user_tel
    return render_template('edit_profile_admin.html', form=form, user=user)
