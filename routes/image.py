import os
import uuid
from models.user import User
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
    jsonify
)
from models.res import Res

main = Blueprint('image', __name__)

@main.route('/upload', methods=['POST'])
def upload():
    """
    1. 通过 session 获取信息
    2. 获取图片信息
    3. 储存图片（单张）
    4. 返回对应信息
    """
    file = request.files
    print('form', file)
    u = User.querUserFromSession()
    print('用户信息', u)
    data = dict(

    )
    r = Res.success(data)
    resp = make_response(jsonify(r))
    return resp
