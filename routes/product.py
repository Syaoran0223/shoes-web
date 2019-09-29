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
from routes import cors, hasToken, formatParams
from models.product import Product
from models.res import Res
from config.base import base_url

main = Blueprint('product', __name__)


@main.route("/", methods=['GET'])
def index():
    # u = current_user()
    return '1234444 product'


@main.route('/addProduct', methods=['POST', 'GET'])
def addProdect():
    form = request.form
    print('发送成功', form)
    data = Product.addProduct(form)    
    print('data', data)
    r = Res.success(data)
    print('发送成功的处理结果jsonify(r)', jsonify(r))
    return make_response(r)


@main.route('/delete', methods=['POST'])
def delete():
    form = request.json

    # data = Img.delete_one(id=form.get('id'))
    # print('delete form', data is None)
    # if data is None:
    # r = Res.success()
    # else:
    # r = Res.fail(msg='图片删除失败')
    # return make_response(jsonify(r))
    return


@main.route('/all', methods=['GET'])
def findAll():
    # form = request.args.to_dict()
    # page_size = form.get('page_size') or None
    # page_index = form.get('page_index') or None
    # data, count = Img.all(page_size=page_size, page_index=page_index)
    # data_json = [d.json() for d in data]
    # for d in data_json:
    #     # format = '%Y-%m-%d %H:%M:%S'
    #     ct = d['created_time']
    #     # d['created_time'] = '{}-{}-{} {}:{}:{}'.format(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)
    #     d['created_time'] = ct.strftime("%Y-%m-%d %H:%M:%S")

    # d = dict(
    #     list=data_json,
    #     count=count
    # )
    # r = Res.success(d)
    # resp = make_response(jsonify(r))
    # return resp
    return


@main.route('/delete', methods=['POST'])
def delete_one():
    return
    # id = request.json.get('id')
    # data = Img.delete_one(id=id)
    # if data is None:
    #     r = Res.success()
    # else:
    #     r = Res.fail()
    # return make_response(jsonify(r))


@main.route('/delete_more', methods=['POST'])
def delete_more():
    # form = request.json
    # print('delete_more form', form)
    # data = Img.delete_by_ids(ids=form['ids'])
    # print('delete_more len', len(data))
    # if len(data) is 0:
    #     r = Res.success()
    # else:
    #     r = Res.fail()
    # return make_response(jsonify(r))
    return


@main.route('/update', methods=['post'])
def update():
    # form = request.json
    # print('form', form)
    # data = Img.update(id=form['id'], show=str(form['enable']))
    # print('data', data)
    # r = Res.success(data)
    # return make_response(jsonify(r))
    return
