import uuid
from sqlalchemy import Column, String, Text, Integer
from config.secret import secret_key
from models.base_model import SQLMixin, db

class Teacher(SQLMixin, db.Model):
    # 名字 头像 职位 介绍 班级类型
    __tablename__ = 'teacher'
    name = Column(String(50), nullable=False, comment='名字')
    avatar = Column(String(50), comment='头像')
    job = Column(String(50), comment='职位')
    introduce = Column(String(50),comment='介绍')
    type = Column(String(2), comment='01:2d班, 02:3d班, 03:基础班')



