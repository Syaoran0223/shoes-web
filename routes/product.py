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
from models.product_attr import ProductAttr
from models.stock import Stock
from models.res import Res
from config.base import base_url
from models.picture import Picture as Img
from config.base import base_url
import xlrd

main = Blueprint('product_router', __name__)


@main.route("/", methods=['GET'])
def index():
    # u = current_user()
    return '1234444 product'


@main.route('/queryProductType', methods=['POST'])
def queryProdcut():
    # 查询商品大类
    r = Product.queryAll()
    r = Res.success(r)
    print('查询所有商品', r)
    return make_response(jsonify(r))


@main.route('/addProductType', methods=['POST'])
def addProductType():
    # form : product_id, bar_code
    form = request.form.to_dict()
    print('form', form)
    # 上传图片
    file = request.files['file']
    if file is not None:
        # 储存图片获取数据
        data = Img.save_one(file, form)
        print('upload data', data)
        if data['src'] is not None and base_url not in data['src']:
            data['src'] = base_url + '/' + data['src']
            form['cover'] = data['src']
        if data is not None:
            r = Res.success(data)
        else:
            r = Res.fail({}, msg='图片已存在')
    print('新图片', form)
    product = Product.add(form)
    if type(product) is str:
        r = Res.fail(msg=product)
    else:
        all = Product.all()
        print('all', all)
        r = Res.success(all)

    return make_response(jsonify(r))


@main.route('/queryProduct', methods=['POST'])
def queryProdcutAttr():
    # 查询对应商品子类
    r = ProductAttr.queryAll()
    r = Res.success(r)
    print('查询所有商品')
    return make_response(jsonify(r))


@main.route('/addProduct', methods=['POST', 'GET'])
def addProduct():
    form = request.form.to_dict()
    print('form', form)
    product_attr = ProductAttr.add(form)
    print('product_attr', product_attr)
    if type(product_attr) is str:
        r = Res.fail(msg=product_attr)
    else:
        r = product_attr
        r = Res.success(product_attr)
    return make_response(jsonify(r))


@main.route('/queryProductByBarCode', methods=['POST'])
def queryProductByBarCode():
    form = request.form.to_dict()
    q = ProductAttr.queryByBarCode(form)
    if len(q) is 0:
        r = Res.fail(q.msg)
    else:
        r = Res.success(q)

    return make_response(jsonify(r))


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


@main.route('/queryProduct', methods=['GET'])
def findAll():
    r = ProductAttr.all()
    print('r', r)
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

# 测试上传excel
# todo excel 内字段不规则 无法直接导入


@main.route("/uploadFile", methods=['POST', 'GET'])
def uploadFile():
    print('接收信息', request.files)
    file = request.files['file']
    print('file', type(file), file)
    print('文件名', file.filename)  # 打印文件名
    print('name', file.name)
    f = file.read()  # 文件内容
    data = xlrd.open_workbook(file_contents=f)
    table = data.sheets()[0]
    names = data.sheet_names()  # 返回book中所有工作表的名字

    status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
    print('导入状态', status)
    nrows = table.nrows  # 获取该sheet中的有效行数
    ncols = table.ncols  # 获取该sheet中的有效列数
    # print('nrows',nrows)
    # print('ncols',ncols)
    s = table.col_values(2)  # 第1列数据
    print('尺码', s)
    table_name = names[0]
    res = formatExcel(table)
    # 根据文件名添加批次
    for r in res:
        r['batch'] = table_name
    
    r = Stock.add_by_count(res)
    # print('导入结果', r)
    return make_response(jsonify(Res.success(r)))


def formatExcel(table):
    # 获取排列长度        
    rowlen = table.nrows
    # 处理头部
    head = formatHeadToSql(table.row_values(0))
    # 结果 临时变量
    result = []
    t = ''
    # 循环列表 补全货号
    for i in range(1, rowlen):
        row = table.row_values(i)
        print('测试', row,)
        # 0 货号 1 备注
        if len(row[0]) == 0:
            row[0] = t[0]
        if len(row[1]) == 0:
            row[1] = t[1]
        t = row
        # 去除货号前后空格
        row[0] = row[0].strip()
        print('完成', row)
        result.append(dict(zip(head, row)))
    return result


def formatHeadToSql(head):
    headMap = dict(
        货号='code',
        备注='name',
        状态='status',
        # 成本='cost',
        出价='cost',
        售价='price',
        运费='express_price',
        利润='profit',
        实际收益='profit',
        订单='order_id',
        批次='batch',
        尺码='size',
        数量='count',
    )
    keyMap = headMap.keys()

    r = []
    for h in head:
        if h != '' and h in keyMap:
            h = headMap[h]
            r.append(h)
    return r
