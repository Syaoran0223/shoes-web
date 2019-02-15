import os
import time
import uuid
from utils import log
from config.base import base_url
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
from models.user import User
from models.res import Res
from models.teacher import Teacher

main = Blueprint('teacher', __name__)

@main.route('/all', methods=['GET'])
def findAll():
    form = request.args.to_dict()
    page_size = form.get('page_size') or None
    page_index = form.get('page_index') or None
    data, count= Teacher.all(page_size=page_size, page_index= page_index)
    data_json = [d.json() for d in data]
    for i in range(0, len(data_json)):
        data_json[i]['created_time'] = data_json[i]['created_time'].strftime("%Y-%m-%d %H:%M:%S")
        data_json[i]['updated_time'] = data_json[i]['updated_time'].strftime("%Y-%m-%d %H:%M:%S")
        print('base_url not in data_json avatar ', base_url not in data_json[i]['avatar'])
        if data_json[i]['avatar'] is not None and base_url not in data_json[i]['avatar']:
            data_json[i]['avatar'] = base_url + data_json[i]['avatar']
    d = dict(
        list=data_json,
        count=count
    )
    print('findAll 数据类型',d)
    r = Res.success(d)
    resp = make_response(jsonify(r))
    return resp

@main.route('/add', methods=['POST'])
def add():
    form = request.json
    print('add form', form)
    # 储存图片获取数据
    data = Teacher.new(form)
    print('new add data', data )
    if data is not None:
        print ('Res, data', data)
        r = Res.success(data.json())
        print('Res r', r)
    else:
        r = Res.fail({}, msg='教师新增失败')
    return make_response(jsonify(r))

@main.route('/delete', methods=['POST'])
def delete():
    form = request.json
    data = Teacher.delete_one(id=form.get('id'))
    print('delete form', data is None)
    if data is None:
        r = Res.success()
    else:
        r = Res.fail(msg='图片删除失败')
    return make_response(jsonify(r))



@main.route('/delete', methods=['POST'])
def delete_one():
    print('delete_one', request.json)
    id = request.json.get('id')
    print('delete one id', id)
    data = Teacher.delete_one(id=id)
    if data is None:
        r = Res.success()
    else:
        r = Res.fail()
    return make_response(jsonify(r))

@main.route('/delete_more', methods=['POST'])
def delete_more():
    form = request.json
    print('delete_more form', form)
    data = Teacher.delete_by_ids(ids=form['ids'])
    print('delete_more len', len(data))
    if len(data) is 0:
        r = Res.success()
    else:
        r = Res.fail()
    return make_response(jsonify(r))

@main.route('/update', methods=['post'])
def update():
    form = request.json
    print('update form', form)
    id = form['id']
    print('update id', id)
    data = Teacher.update(**form)
    print('data', data)
    r = Res.success(data)
    return make_response(jsonify(r))

@main.route('/query_by_name', methods=['GET'])
def queryImageByName():
    form = request.args.to_dict()
    print('根据标题搜索数据', form)
    data, count = Teacher.queryByCondition(**form)
    d = dict(
        list=data,
        count=count
    )
    r = Res.success(d)
    print('queryImageByName 结果', r)
    return make_response(jsonify(r))
