import hashlib

from sqlalchemy import Column, String, Text, Integer
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
    username = Column(String(50))
    key = Column(String(100))
    value = Column(String(100))
    note = Column(String(100), comment='备注')
    table= Column(String(100), comment='对应表')


