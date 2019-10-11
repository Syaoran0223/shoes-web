import hashlib
import datetime


from sqlalchemy import Column, String, Text, Float, Integer, text, DateTime
from models.base_model import SQLMixin, db


class Batch(SQLMixin, db.Model):
    # 批次表 库存表
    __tablename__ = 'batch'
    name = Column(String(50), comment='名称')
    # 参与人员 比例
    proportion = Column(String(50), comment='比例')
    # 进货时间
    purchase_time = Column(DateTime, comment='进货时间')


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