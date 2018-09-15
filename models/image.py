import hashlib
import os

from sqlalchemy import Column, String, Text
from config.secret import secret_key
from models.base_model import SQLMixin, db
from PIL import Image
from flask import (
    url_for
)


class Img(SQLMixin, db.Model):
    __tablename__ = 'image'
    file_name = Column(String(50), nullable=False)
    src = Column(String(100), nullable=False)
    width = Column(String(100), nullable=False)
    height = Column(String(20), nullable=False)
    hash = Column(String(100), nullable=True, default='')

    @classmethod
    def save_one(cls, img):
        basedir = os.path.abspath(os.path.join(os.getcwd(), ""))
        base_url = '\\static\\'
        # path = basedir + "\\upload_image\\"
        # path = basedir + "/upload_image/"
        path = basedir+ base_url
        # print('path', path)
        file_path = path + img.filename
        print('file_path', file_path)
        # 获取图片信息
        img.save(file_path)
        img_size = Image.open(img).size
        print('img_size', img_size)
        data = dict(
            file_name=img.filename,
            width=img_size[0],
            height=img_size[1],
            src= base_url + img.filename
        )
        r = cls.new(data).json()
        print('Image save_one', r)
        return r
