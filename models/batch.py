import hashlib

from sqlalchemy import Column, String, Text, Float, Integer, text
from models.base_model import SQLMixin, db


class Stock(SQLMixin, db.Model):
    # 批次表 库存表
    __tablename__ = 'batch'
    batch = Column(String(50),comment='批次', nullable=False)
    code = Column(String(50), comment='编码')
    name = Column(String(50), nullable=False, comment='名称')
    proportion = Column(Float, comment='比例')


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