import os
import time
import uuid

from models.user import User
from routes import (
    current_user,
    login_required,
)
from models.batch import Batch
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

main = Blueprint('stock_routes', __name__)


@main.route("/", methods=['GET'])
def index():
    # u = current_user()
    return 'api from stock_routes'


@main.route('/queryByBatch', methods=['POST'])
@login_required
def queryByBatch():
    # 查询商品大类
    form = request.form.to_dict()
    id = form.get('id')
    r = Stock.queryAll(id=id)
    r = Res.success(r)
    print('查询所有商品', r)
    return make_response(jsonify(r))

@main.route('/queryByCondition', methods=['POST'])
def queryByCondition():
    form = request.form.to_dict()
    r = Stock.all(**form)
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


@main.route('/updateStock', methods=['post'])
def update():
    form = request.form.to_dict()
    form['editor'] = session.get('id')
    data = Stock.update(**form)
    print('data', data)
    r = Res.success(data)
    return make_response(jsonify(r))


# 测试上传excel
# todo excel 内字段不规则 无法直接导入

@main.route("/uploadFile", methods=['POST', 'GET'])
def uploadFile():
    form = request.form.to_dict()
    id = form.get('id')
    print('上传接受的参数', form)
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
    Batch.update(id=id, upload=1, excel_name=form.get('excel_name'))
    Stock.delete_by_batch_id(id=id)
    res = formatExcel(table)
    # 根据文件名添加批次
    for r in res:
        r['batch'] = form.get('id')

    r = Stock.add_by_list(res)
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
        print('测试', row, )
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
        名称='name',
        状态='status',
        备注='note',
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
