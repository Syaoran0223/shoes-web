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
from PIL import Image
from routes import cors, hasToken, formatParams
from models.user import User
from models.res import Res
from config.base import base_url

from models.picture import Picture as Img
main = Blueprint('image', __name__)

@main.route('/upload', methods=['POST'])
def upload():
    form = request.files['file']
    # 储存图片获取数据
    data = Img.save_one(form)
    print('upload data', data)
    if data['src'] is not None and base_url not in data['src']:
        data['src'] = base_url + '/' + data['src']
    if data is not None:
        r = Res.success(data)
    else:
        r = Res.fail({}, msg='图片已存在')
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
    form = request.args.to_dict()
    page_size = form.get('page_size') or None
    page_index = form.get('page_index') or None
    data, count= Img.all(page_size=page_size, page_index= page_index)
    data_json = [d.json() for d in data]
    for d in data_json:
        # format = '%Y-%m-%d %H:%M:%S'
        ct= d['created_time']
        # d['created_time'] = '{}-{}-{} {}:{}:{}'.format(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)
        d['created_time'] = ct.strftime("%Y-%m-%d %H:%M:%S")

    d = dict(
        list=data_json,
        count=count
    )
    r = Res.success(d)
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
def delete_more():
    form = request.json
    print('delete_more form', form)
    data = Img.delete_by_ids(ids=form['ids'])
    print('delete_more len', len(data))
    if len(data) is 0:
        r = Res.success()
    else:
        r = Res.fail()
    return make_response(jsonify(r))

@main.route('/update', methods=['post'])
def update():
    form = request.json
    print('form', form)
    data = Img.update(id=form['id'], show=str(form['show']))
    print('data', data)
    r = Res.success(data)
    return make_response(jsonify(r))

@main.route('/queryImageByName', methods=['GET'])
def queryImageByName():
    form = request.args.to_dict()
    print('根据标题搜索数据', form)
    data, count = Img.queryByCondition(**form)
    d = dict(
        list=data,
        count=count
    )
    r = Res.success(d)
    print('queryImageByName 结果', r)
    return make_response(jsonify(r))
