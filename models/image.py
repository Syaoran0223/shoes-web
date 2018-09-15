import hashlib

from sqlalchemy import Column, String, Text
from config.secret import secret_key
from models.base_model import SQLMixin, db



class Image(SQLMixin, db.Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    __tablename__ = 'image'
    """
    
    """
    file_name = Column(String(50), nullable=False)
    width = Column(String(100), nullable=False)
    height = Column(String(100), nullable=False)
    author = Column(String(20), default='匿名')
    src = Column(String(100), nullable=False)
    hash = Column(String(100))

