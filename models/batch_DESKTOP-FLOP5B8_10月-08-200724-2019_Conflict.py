import hashlib

from sqlalchemy import Column, String, Text, Float, Integer, text
from models.base_model import SQLMixin, db


class Batch(SQLMixin, db.Model):
    # 批次表 库存表
    __tablename__ = 'batch'
    name = Column(String(50), nullable=False, comment='名称')        
    batch = Column(String(50), comment='批次')


    @classmethod
    def add_by_count(cls, form):
        print('商品参数详情', form)
        p = cls.new_by_list(form)
        return p

    @classmethod
    def queryAll(cls):
        sql = """
       SELECT * from batch      
        """        
        sql = text(sql)
        p = cls.query.session.execute(sql)
        list = cls.sql_to_list(p)
        return list
