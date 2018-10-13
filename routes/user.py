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
    print('login, u', u)
    if u is not None:
        token = u.json().get('token')
        print('token', token)
        session['user_id'] = u.id
        print('session', session)
        print('login session', session.get('user_id'))
        # 设置 cookie 有效期为 永久
        session.permanent = True
        token = dict(
            token = token
        )
        r = Res.success(token,msg='登录成功')
    else:
        r = Res.fail({}, '登录失败')
    resp = make_response(jsonify(r))
    resp.headers["X-Token"] = [token.get('token')]
    return resp


@main.route('/info', methods=['GET'])
@hasToken
def queryUserInfo(*args, **kwargs):
    print('session', session)
    # uid = session.get('user_id')
    uid = 1
    print('queryUserInfo uid', uid)
    u = User.one(id=uid)
    print('queryUserInfo u', u)
    data = dict(
        roles = [u.token],
        name = u.username,
        avatar = 'http://thirdwx.qlogo.cn/mmopen/hgXWbMaaqmAj8fAKJJq1nozVgMrm7CfOd7w1W7UleKwFJT2dQbE7W9qRWr04Zra7W1PRQ5fibRZgqr7myOiadx6Q/132',
    )
    r = Res.success(data)
    resp = make_response(jsonify(r))
    return resp

