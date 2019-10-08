import hashlib

from sqlalchemy import Column, String, Text, Float, Integer, text
from models.base_model import SQLMixin, db


class Stock(SQLMixin, db.Model):
    __tablename__ = 'shoes_stock'
    code= Column(String,comment='货号')
    name = Column(String, comment='备注')
    product_id = Column(Integer, comment='产品id')
    status = Column(Integer, comment='0：待发货，1：发货，3瑕疵', default=0)
    cost = Column(Float, comment='进价')
    price = Column(Float, comment='售价')
    express_price = Column(Float,comment='运费')
    profit = Column(Float,comment='利润')
    order_id = Column(String(50), comment='所属订单')
    batch = Column(String(50),comment='批次')

    @classmethod
    def add_by_count(cls,form):
        # params:
        #   status 0
        #   cost 0
        #   count 1
        #   product id
        print('商品参数详情', form)
        p = cls.new_by_count(form)
        print('新增鞋子', p)
        return p

    @classmethod
    def queryAll(cls):
        sql = """
        SELECT * FROM product p 
        LEFT JOIN product_attr pa on p.id = pa.product_id 
        LEFT JOIN shoes_stock s on s.product_id = p.id  
        WHERE s.product_id = {}      
        """.format(1)
        print('sql语句', sql)
        sql = text(sql)
        p = cls.query.session.execute(sql)
        list = cls.sql_to_list(p)
        return list
