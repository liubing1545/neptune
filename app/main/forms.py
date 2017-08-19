# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as FlaskForm
from wtforms import StringField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Regexp
from wtforms import ValidationError
from ..models import User


# 用户更改个人信息表单
# 属性：tel 电话，submit 提交
class EditProfileForm(FlaskForm):
    tel = StringField(
        u'电话号码', validators=[Required(), Length(11), Regexp('^[0-9]*$')])
    submit = SubmitField(u'提交')


# 管理员更改用户信息表单
# 属性：username 用户名，confirmed 是否认证账户，role 用户类型，tel 电话，
#       submit 提交
class EditProfileAdminForm(FlaskForm):
    username = StringField(
        u'用户名',
        validators=[
            Required(), Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters, '
                   'numbers, dots or underscores')
        ])
    role = SelectField(u'类型', coerce=int)
    tel = StringField(
        u'电话号码', validators=[Required(), Length(11), Regexp('^[0-9]*$')])
    submit = SubmitField(u'提交')

    # 初始化表单，添加性别选项
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.user = user

    # 验证用户名
    def validate_user_name(self, field):
        if field.data != self.user.user_name and \
                User.query.filter_by(user_name=field.data).first():
            raise ValidationError(u'该用户名已被注册.')
