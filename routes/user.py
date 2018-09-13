import os
import uuid

from utils import log
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory,
    jsonify,
)

from routes import cors, hasToken
from models.user import User
from models.res import Res
main = Blueprint('user', __name__)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    u = User.register(form)
    print('注册', u)    
    return jsonify(u)

@main.route("/login", methods=['POST'])
def login():
    print('request.header', request.headers)
    # form = request.form
    form = request.json
    print('form', form)
    u = User.validate_login(form)
    token = u.json().get('token')
    if u is not None:
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        token = dict(
            token = token
        )
        r = Res.success(token, '登录成功')
    else:
        r = Res.fail({}, '登录失败')
    resp = make_response(jsonify(r))
    resp.headers["X-Token"] = [token.get('token')]
    return resp


@main.route('/info', methods=['GET'])
@hasToken
def queryUserInfo():
    print('request.header', request.headers.get('X-Token'))
    print('cookie', request.cookies)
    uid = session.get('user_id')
    u = User.one(id=uid)
    print('uid', u)
    data = dict(
        roles = [u.token],
        name = u.username,
        avatar = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80',
    )
    r = Res.success(data)
    resp = make_response(jsonify(r))
    return resp
