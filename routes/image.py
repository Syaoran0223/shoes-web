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

    jsonify
)
from models.res import Res

main = Blueprint('image', __name__)
from PIL import Image
from routes import cors, hasToken
from models.user import User
from models.res import Res
from models.picture import Picture
main = Blueprint('image', __name__)


@main.route('/upload', methods=['POST'])
def uplpad():
    form = request.files['file']
    # 储存图片获取数据
    data = Picture.save_one(form)
    if data is not None:
        r = Res.success(data)
    else:
        r = Res.fail({})
    return make_response(jsonify(r))

@main.route('/delete', methods=['POST'])
def delete():
    form = request.json
    data = Picture.delete_one(id=form.get('id'))
    print('delete form', data is None)
    if data is None:
        r = Res.success()
    else:
        r = Res.fail(msg='图片删除失败')
    return make_response(jsonify(r))

@main.route('/all', methods=['GET'])
def findAll():
    data = Picture.all()
    data_json = [d.json() for d in data]
    r = Res.success(data_json)
    resp = make_response(jsonify(r))
    return resp


