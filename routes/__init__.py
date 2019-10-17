from functools import wraps

from flask import session, request, abort, make_response, jsonify

from models.res import Res
from models.user import User, identity_map
from utils import log
# from models.session import Session

def cors(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        r = make_response(func(*args, **kwargs))
        r.headers['Access-Control-Allow-Origin'] = 'http://localhost:9528'
        r.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
        allow_headers = "Referer, Accept, Origin, User-Agent, X-Requested-With, Content-Type, Cookie"
        r.headers['Access-Control-Allow-Headers'] = allow_headers
        # if you need the cookie access, uncomment this line
        r.headers['Access-Control-Allow-Credentials'] = 'true'
        return r
    return wrapper_func

def hasToken(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('*args', args)
        print('**kwargs', kwargs)
        token = request.headers.get('X-Token')
        print('hasToken', token)
        if token is not None:
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper

def formatParams(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('判断方法', request.method)
        if request.method == 'GET':
            form = request.args.to_dict()
        elif request.method == 'POST':
            form = request.json
        for f in form:
            kwargs[f] = form.get(f)
        # print('*args', args)
        # print('**kwargs', kwargs)
        return func(*args, **kwargs)
    return wrapper


def current_user():
    log('真正的sesson', session)
    user_id = session.get('id')
    log('current session获取的id', user_id)
    if user_id is not None:
        u = User.one(id=user_id)
        log('查询结果', u)
        return u.json()
    else:
        log('没进去')
        return make_response(jsonify(Res.fail('没有权限')))

def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """
    @wraps(route_function)
    def f():
        log('是否进入登录判断')
        u = current_user()
        log('判断用户', u)
        log('用户权限', u.get('identity'), '管理员权限', identity_map.get('admin'))
        if u.get('identity') == identity_map.get('admin') or u.get('identity') == identity_map.get('tester'):
            log('登录用户', route_function)
            return route_function()

        else:
            log('游客用户')
            r = Res.fail(u, msg='不是管理员用户')
            return make_response(jsonify(r))
    return f