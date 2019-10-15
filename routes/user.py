import os
import uuid
from config import base
import requests

from models.session import Session
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
    form = request.form.to_dict()
    wxloginUrl = """https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appSecret}&js_code={code}&grant_type=authorization_code""".format(appid=base.appid, appSecret=base.appSecret, code=form.get('code'))
    res = requests.post(wxloginUrl).json()
    u = User.login(res)
    print('u', u)
    filterMap = ['openid', 'id','updated_time']
    if u is not None:
        token = u.get('token')
        print('token', token)
        sform = dict(
            session_id=u.get('openid'),
            user_id= u.get('id')
        )
        print('ssssform', sform)
        s = Session.add(sform)
        log('生成的 session', s)
        session['user_id'] = u.get('openid')
        print('session', session)
        print('login session', session.get('user_id'))
        # 设置 cookie 有效期为 永久
        session.permanent = True
        token = dict(
            token=token
        )
    result = dict()
    for k in u.keys():
        if  k in filterMap:
            result[k] = u[k]
    resp = make_response(jsonify(result))
    resp.headers["X-Token"] = [token.get('token')]
    print('resp in login', resp.headers)
    return resp


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
            token=token
        )
        r = Res.success(token, msg='登录成功')
    else:
        r = Res.fail({}, '登录失败')
    print('r',jsonify(r))
    resp = make_response(jsonify(r))

    resp.headers["X-Token"] = [token.get('token')]
    return resp


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
