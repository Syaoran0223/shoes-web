import os
import time
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
from models.picture import Picture as Img
main = Blueprint('image', __name__)


@main.route('/upload', methods=['POST'])
def uplpad():
    form = request.files['file']
    # 储存图片获取数据
    data = Img.save_one(form)
    if data is not None:
        r = Res.success(data)
    else:
        r = Res.fail({}, msg='图片上传失败/有同样 hash的图片')
    return make_response(jsonify(r))

@main.route('/delete', methods=['POST'])
def delete():
    form = request.json
    data = Img.delete_one(id=form.get('id'))
    print('delete form', data is None)
    if data is None:
        r = Res.success()
    else:
        r = Res.fail(msg='图片删除失败')
    return make_response(jsonify(r))

@main.route('/all', methods=['GET'])
def findAll():
    data = Img.all()
    data_json = [d.json() for d in data]
    for d in data_json:
        format = '%Y-%m-%d %H:%M:%S'
        temp_time=time.localtime(d['created_time'])
        d['created_time'] = time.strftime(format, temp_time)
    r = Res.success(data_json)
    resp = make_response(jsonify(r))
    return resp


@main.route('/delete', methods=['POST'])
def delete_one():
    id = request.json.get('id')
    data = Img.delete_one(id=id)
    if data is None:
        r = Res.success()
    else:
        r = Res.fail()
    return make_response(jsonify(r))

@main.route('/delete_more', methods=['POST'])
def delete_more(**kwargs):
    form = request.json
    print('delete_more form', form)
    data = Img.delete_by_ids(ids=form['ids'])
    if len(data) is 0:
        r = Res.success()
    else:
        r = Res.fail()
    return make_response(jsonify(r))

@main.route('/update', methods=['post'])
def update():
    form = request.json
    print('updata form', form)
    data = Img.update(id=form['id'], show=str(form['show']))
    print('data', data)
    r = Res.success(data)
    return make_response(jsonify(r))