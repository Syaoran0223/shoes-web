import hashlib

from sqlalchemy import Column, String, Text, Float, Integer
from sqlalchemy.dialects.mysql import json

from config.secret import secret_key
from models.base_model import SQLMixin, db
from sqlalchemy import text, func

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
# 百度 ocr
# from aip import AipOcr
# config = {
#     'appId': '17395577',
#     'apiKey': 'pv0I52bS92oXlqigWGsTK4pG',
#     'secretKey': 'Gy3rX85ijRlkv3vgtQfGQwwxBAS5RBYg'
# }
#
# client = AipOcr(**config)

class Product(SQLMixin, db.Model):
    __tablename__ = 'product'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    level 有两个属性 'admin', 'edit'
    """
    name = Column(String(50), nullable=False, comment='鞋子名称')
    code = Column(String(50), comment='鞋子编码')
    cover = Column(String(500), comment='展示图')
    note = Column(String(50), comment='简称')
    # bar_code = Column(String(50))
    # password = Column(String(100), nullable=False)
    # avatar = Column(String(200), nullable=False, default='/images/3.jpg')
    # token = Column(String(20), nullable=False, default='edit')
    @classmethod
    def isExist(cls, form):
        return

    @classmethod
    def add(cls, form):
        print('form', form)
        query = cls.one(code=form['code'])
        print('查找重复', query)
        if query is None:
            p = cls.new(form)
        else:
            p = '已存在该商品类型'
        return p

    @classmethod
    def queryAll(cls):
        sql = """
        SELECT * from product        
        """
        sql = text(sql)
        res = db.engine.execute(sql)
        list = cls.sql_to_list(res)
        return list

    @classmethod
    def delete(cls):
        return



