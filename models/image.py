import hashlib
import os

from sqlalchemy import Column, String, Text
from config.secret import secret_key
from models.base_model import SQLMixin, db
from PIL import Image

class Img(SQLMixin, db.Model):
    __tablename__ = 'image'
    file_name = Column(String(50), nullable=False)
    src = Column(String(100), nullable=False)
    width = Column(String(100), nullable=False)
    height = Column(String(20), nullable=False)

    @classmethod
    def save_one(cls, img):
        basedir = os.path.abspath(os.path.join(os.getcwd(), "../"))
        path = basedir + "\\upload_image\\"
        file_path = path + img.filename
        print('file_path', file_path)
        # 获取图片信息
        img.save(file_path)
        # 获取图片大小
        img_size = Image.open(img).size
        print('img_size', img_size)
        data = dict(
            file_name=img.filename,
            width=img_size[0],
            height=img_size[1],
            src = file_path
        )
        r = cls.new(data)
        print('Image save_one', r)
        return r
