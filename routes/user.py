import os
import uuid
from config import base
import requests

# from models.session import Session
from models.user_role import UserRole

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
    print('login before session', session)
    form = request.form.to_dict()
    wx_login_url = """https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appSecret}&js_code={code}&grant_type=authorization_code""".format(appid=base.appid, appSecret=base.appSecret, code=form.get('code'))
    res = requests.post(wx_login_url).json()
    u = User.login(res)
    print('u', u)
    session['id'] = u.get('id')
    # session[u.get('openid')] = u.get('id')
    print('session in login', session)
    filter_map = ['openid', 'id', 'updated_time']
        # 设置 cookie 有效期为 永久
        # session.permanent = True
    result = dict()
    for k in u.keys():
        if k in filter_map:
            result[k] = u[k]
    resp = make_response(jsonify(result))
    # resp.headers["X-Token"] = [token.get('token')]
    # print('resp in login', resp.headers)
    return resp


    # u = User.validate_login(form)
    # print('login, u', u)
    # if u is not None:
    #     token = u.json().get('token')
    #     print('token', token)
    #     session['user_id'] = u.id
    #     print('session', session)
    #     print('login session', session.get('user_id'))
    #     # 设置 cookie 有效期为 永久
    #     session.permanent = True
    #     token = dict(
    #         token=token
    #     )
    #     r = Res.success(token, msg='登录成功')
    # else:
    #     r = Res.fail({}, '登录失败')
    # print('r',jsonify(r))
    # resp = make_response(jsonify(r))
    #
    # resp.headers["X-Token"] = [token.get('token')]
    # return resp


@main.route('/info', methods=['GET'])
@hasToken
def queryUserInfo(*args, **kwargs):
    print('session', session)
    uid = session.get('user_id')    # uid = 1
    print('queryUserInfo uid', uid)
    u = User.one(id=uid)
    print('queryUserInfo u', u)
    data = dict(
        roles=[u.token],
        name=u.username,
        avatar=u.avatar,
    )
    r = Res.success(data)
    resp = make_response(jsonify(r))
    return resp
