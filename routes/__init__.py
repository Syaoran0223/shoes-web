from functools import wraps

from flask import session, request, abort,make_response


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