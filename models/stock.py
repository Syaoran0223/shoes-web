import hashlib

from sqlalchemy import Column, String, Text, Float, Integer, text
from models.base_model import SQLMixin, db


class Stock(SQLMixin, db.Model):
    __tablename__ = 'stock'
    product_id = Column(Integer, comment='产品id')
    batch = Column(String(50),comment='批次')
    code = Column(String(50), comment='货号')
    note= Column(String(100), comment='备注')
    size = Column(Float, comment='尺码')
    status = Column(Integer, comment='0：待发货，1：发货，3瑕疵', default=0)
    cost = Column(Float, comment='进价')
    price = Column(Float, comment='售价')
    express_price = Column(Float,comment='运费')
    profit = Column(Float,comment='利润')
    express_number = Column(String(50), comment='订单号')

    @classmethod
    def add_by_list(cls,form):
        # params:
        #   status 0
        #   cost 0
        #   count 1
        #   product id
        print('商品参数详情', form)
        p = cls.new_by_list(form)
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