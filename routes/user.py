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
from routes import cors
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
        r = Res.success(token, '今次 我便是要看看这登录可否成功！')
    else:
        r = Res.fail({}, '登录失败')
    resp = make_response(jsonify(r))
    resp.headers["X-Token"] = [token.get('token')]
    return resp


@main.route('/info', methods=['GET'])
def queryUserInfo():
    print('cookie', request.cookies)
    return