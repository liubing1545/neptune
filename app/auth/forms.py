# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


# 用户登录表单
# 属性：email 邮箱，password 密码，remember_me 是否下次自动登录，submit 提交
class LoginForm(Form):
    email = StringField(
        u'邮箱',
        validators=[Required(), Length(1, 64), Email()],
        render_kw={"placeholder": u"邮箱"})
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'下次自动登录')
    submit = SubmitField(u'登录')


# 用户注册表单
# 属性：user_email 邮箱，user_name 用户名，user_eid 用户工作号，password 密码，
#       password2 确认密码，user_tel 用户电话，submit 提交
class RegistrationForm(Form):
    user_email = StringField(
        u'邮箱', validators=[Required(), Length(1, 64), Email()])
    user_name = StringField(
        u'用户名',
        validators=[
            Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              u'用户名只能包含数字，字母，下划线或点')
        ])
    user_eid = StringField(
        u'员工号', validators=[Required(), Regexp('^[0-9]*$', 0, u'请输入数字')])
    password = PasswordField(
        u'密码', validators=[Required(), EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    user_tel = StringField(
        u'电话',
        validators=[
            Required(), Length(8, 11), Regexp('^[0-9]*$', 0, u'请输入数字')
        ])
    submit = SubmitField(u'注册')

    # 验证邮箱
    def validate_user_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError(u'此邮箱已被注册')

    # 验证用户名
    def validate_user_name(self, field): 
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError(u'此用户名已被注册')

    # 验证员工号
    def validate_user_eid(self, field):
        if User.query.filter_by(user_eid=field.data).first():
            raise ValidationError(u'此员工号已被注册')

    # 验证电话号码
    def validate_user_tel(self, field):
        if User.query.filter_by(user_tel=field.data).first():
            raise ValidationError(u'电话号码已被注册')


# 用户更改密码表单
# 属性：old_password 原始密码，password 新密码，password2 确认新密码，submit 提交
class ChangePasswordForm(Form):
    old_password = PasswordField(u'请输入密码', validators=[Required()])
    password = PasswordField(
        u'新密码',
        validators=[Required(), EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'更改密码')


# 用户找回密码请求表单
# 属性：email 邮箱，submit 提交
class PasswordResetRequestForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField(u'重置密码')


# 用户重置密码表单
# 属性：email 邮箱，password 重置密码，password2 确认重置密码，submit 提交
class PasswordResetForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(
        u'新密码',
        validators=[Required(), EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'重置密码')

    # 验证邮箱
    def validate_email(self, field):
        if User.query.filter_by(user_email=field.data).first() is None:
            raise ValidationError(u'无法识别此邮箱')


# 用户更高邮箱表单
# 属性：email 新邮箱，password 密码，submit 提交
class ChangeEmailForm(Form):
    email = StringField(
        u'新邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'更新邮箱')

    # 验证邮箱
    def validate_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError(u'此邮箱已被注册')
