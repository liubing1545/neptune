# -*- coding: utf-8 -*-
from functools import wraps
from flask import abort
from flask_login import current_user as current_user
from .models import Permission


# 检验用户权限的自定义修饰器
# Params：permission 权限
# Returns：若用户没有制定权限，返回403错误码
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# 检验管理员权限
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
