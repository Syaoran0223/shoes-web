import hashlib
import os
import uuid

from sqlalchemy import Column, String, Text
from config.secret import secret_key
from models.base_model import SQLMixin, db
from PIL import Image
from flask import (
    url_for
)
import socket

class Img(SQLMixin, db.Model):
    __tablename__ = 'image'
    file_name = Column(String(50), nullable=False)
    src = Column(String(100), nullable=False)
    width = Column(String(100), nullable=False)
    height = Column(String(20), nullable=False)
    hash = Column(String(100), nullable=True, default='')
    # 1 代表 true 显示图片
    show =Column(String(1), nullable=False, default=1)

    @classmethod
    def save_one(cls, img):
        suffix = img.filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        path = os.path.join('static/images', filename)
        print('file_path', path)
        print('socket', socket)
        # 获取图片信息
        img.save(path)
        img_size = Image.open(img).size
        print('img_size', img_size)
        data = dict(
            file_name= filename,
            # origin_name=img.filename,
            width=img_size[0],
            height=img_size[1],
            src= path,
        )
        r = cls.new(data).json()
        print('Image save_one', r)
        return r
