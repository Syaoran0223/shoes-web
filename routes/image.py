import os
import uuid
<<<<<<< HEAD
from models.user import User
=======

from utils import log
>>>>>>> 8bf9e695b1c5b528aa92ee86bb2f0768e87325cb
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
<<<<<<< HEAD
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
=======
    jsonify,
)
from PIL import Image
from routes import cors, hasToken
from models.user import User
from models.res import Res
from models.image import Img as Img
main = Blueprint('image', __name__)


@main.route('/upload', methods=['POST'])
def uplpad():
    form = request.files['file']
    # 获取上级目录， 拼接地址
    data = Img.save_one(form)
    if data is not None:
        r = Res.success(data)
    else:
        r = Res.fail({})
    return make_response(jsonify(r))
>>>>>>> 8bf9e695b1c5b528aa92ee86bb2f0768e87325cb
