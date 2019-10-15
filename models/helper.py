import functools
import time

from flask import (
    url_for,
    redirect,
    session,
)

from models.user import User
from utils import log


def current_user():
    if 'user_id' in session:
        user_id = int(session['user_id'])
        u = User.one(id=user_id)
        return u
    else:
        return User.guest()


def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect(url_for('user.login_view'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def formatted_time(current_time):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(current_time)
    formatted = time.strftime(time_format, localtime)
    return formatted
