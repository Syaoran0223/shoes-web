import os
import uuid
from config import base
import requests

# from models.session import Session


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
    print('form', form)
    # https://api.weixin.qq.com/sns/jscode2session?appid=wx4dea673b058fd1a8&secret=4cf491eb3dfc206fe6a7e5d8d47e8c48&js_code=0611WVUD1mB715023RWD1wOEUD11WVUl&grant_type=authorization_code
    wx_login_url = """https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appSecret}&js_code={code}&grant_type=authorization_code""".format(appid=base.appid, appSecret=base.appSecret, code=form.get('code'))
    res = requests.post(wx_login_url).json()
    u = User.login(res)
    # 判断是否为管理员
    is_admin = u.is_admin()
    print('is_admin', is_admin)
    u = u.json()
    session['id'] = u.get('id')
    if is_admin is False:
        return make_response(jsonify(Res.fail(u, msg='不是管理员账户')))
    # 设置 cookie 有效期为 永久
    session.permanent = True
    # 筛选需要返回的数据
    filter_map = ['openid', 'id', 'updated_time', 'identity']
    result = dict()
    for k in u.keys():
        if k in filter_map:
            result[k] = u[k]
    resp = make_response(jsonify(Res.success(result)))
    return resp

@main.route("/loginByAccount", methods=['POST'])
def login_by_account():
    form = request.form.to_dict()
    wx_login_url = """https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appSecret}&js_code={code}&grant_type=authorization_code""".format(appid=base.appid, appSecret=base.appSecret, code=form.get('code'))
    res = requests.post(wx_login_url).json()
    print('res', res)
    u = User.one(username=form.get('username'), password=form.get('password')).json()
    print('帐号登录', u)
    u = User.update(id=u.get('id'), openid=res.get('openid'))
    if u is None:
        return make_response(jsonify(Res.fail(msg='帐号密码错误')))
    else:
        session['id'] = u.get('id')
        return make_response(jsonify(Res.success(u)))


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
