from functools import wraps

from flask import session, request, abort, make_response, jsonify

from models.res import Res
from models.user import User
from utils import log
from models.session import Session

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
    if 'user_id' in session:
        session_id = session.get('user_id')
        print('这里的 session', session_id)
        # s = User.one(openid=session_id)
        # log('session找的用户', s)
        # log('sessionid', session_id)
        s = Session.one(session_id=session_id)
        # log('current_user session', s)
        # log('s.expired', s.expired())
        if s is None or s.expired():
            log('判断当前用户', s)
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        log('没进去')
        return User.guest()

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
        if u.is_guest():
            log('游客用户')
            r = Res.fail(u.json())
            return make_response(jsonify(r))
        else:
            log('登录用户', route_function)
            return route_function()
    return f