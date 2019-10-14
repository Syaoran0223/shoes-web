import hashlib

from sqlalchemy import Column, String, Text, Float, Integer, text
from models.base_model import SQLMixin, db


class Stock(SQLMixin, db.Model):
    __tablename__ = 'stock'
    product_id = Column(Integer, comment='产品id', default=99999)
    batch = Column(String(50),comment='批次')
    code = Column(String(50), comment='货号')
    name = Column(String(100), comment='名称')
    note = Column(String(100), comment='备注')
    size = Column(Float, comment='尺码')
    status = Column(Integer, comment='0：待发货，1：发货，3瑕疵', default=0)
    cost = Column(Float, comment='进价')
    price = Column(Float, comment='售价')
    express_price = Column(Float,comment='运费')
    profit = Column(Float,comment='利润')
    express_number = Column(String(50), comment='订单号')

    @classmethod
    def add_by_list(cls,form):
        print('商品参数详情', form)
        p = cls.new_by_shoes_excel(form)
        print('新增鞋子', p)
        return p

    @classmethod
    def queryAll(cls, id):
        
        sql = """
            select * from stock where batch={}      
        """.format(id)
        print('sql语句', sql)
        sql = text(sql)
        p = cls.query.session.execute(sql)
        list = cls.sql_to_list(p)
        return list
    
    @classmethod    
    def queryByBatch(cls):
        # 测试接口 返回批次货物 状态
        sql = """SELECT batch, status, COUNT(id), SUM(cost) FROM stock 
        GROUP BY batch, status"""
        return ''

    @classmethod
    def delete_by_batch_id(cls, id):
        sql = """DELETE FROM stock  WHERE batch={}""".format(id)
        sql = text(sql)
        print('删除语句', sql)
        p = cls.query.session.execute(sql)

        # list = cls.sql_to_list(p)
        print('删除返回什么', p)
        return True
