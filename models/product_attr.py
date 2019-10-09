import hashlib

from sqlalchemy import Column, String, Text, Float, Integer, text
from config.secret import secret_key
from models.base_model import SQLMixin, db
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)


class ProductAttr(SQLMixin, db.Model):
    __tablename__ = 'product_attr'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    level 有两个属性 'admin', 'edit'
    """
    product_id = Column(Integer, comment='产品id')
    bar_code = Column(String(50), comment='鞋盒条形码')
    size = Column(Float, comment='尺寸-EUR')

    @classmethod
    def add(cls,form):
        query = cls.one(bar_code=form['bar_code'])
        print('查找重复', query)
        if query is None:
            p = cls.new(form)
            print('新增', p)
        else:
            p = '已存在该商品类型'
        return p

    @classmethod
    def queryByBarCode(cls, form):
        sql = """
        SELECT* from  product p
        LEFT JOIN product_attr on p.id = product_attr.product_id
        WHERE bar_code = '{}'
        """.format(form.get('bar_code'))
        sql = text(sql)
        res = db.engine.execute(sql)
        res = cls.sql_to_list(res)
        if len(res) == 0:
            p = '当前没有该商品'
        else:
            p = res[0]
        return p

    @classmethod
    def queryAll(cls):
        sql = """
              SELECT * from product p 
              LEFT JOIN product_attr pa 
              on  p.id = pa.product_id  
              ORDER BY size   
              """
        sql = text(sql)
        res = db.engine.execute(sql)
        list = cls.sql_to_list(res)
        return list

        return p