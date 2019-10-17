import hashlib

from sqlalchemy import Column, String, Text, Integer, text
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


class DictMap(SQLMixin, db.Model):
    __tablename__ = 'dict_map'
    """
    这是一个字典表 用于查找 key value 以及介绍
    """    
    key = Column(String(100))
    value = Column(String(100))
    type = Column(String(100), comment="对应表的字段")
    note = Column(String(100), comment='备注')    
    status = Column(Integer, comment='是否使用')
    alias = Column(String(100), default='')

    @classmethod
    def query_config(cls):
        sql = """
        SELECT d.`key`,d.alias,  d.value, d.type FROM dict_map d WHERE `status` = 0
        """
        sql = text(sql)
        res = db.engine.execute(sql)
        res = cls.sql_to_list(res)
        return res

