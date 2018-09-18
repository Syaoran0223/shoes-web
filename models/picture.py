import hashlib
import os
import uuid
import base64
from sqlalchemy import Column, String, Text
from config.secret import secret_key
from models.base_model import SQLMixin, db

from PIL import Image
from flask import (
    url_for
)
import socket


class Picture(SQLMixin, db.Model):
    __tablename__ = 'image'
    file_name = Column(String(50), nullable=False)
    src = Column(String(100), nullable=False)
    width = Column(String(100), nullable=False)
    height = Column(String(20), nullable=False)
    origin_name = Column(String(50), nullable=False)
    hash = Column(String(100), nullable=True, default='')
    # 1 代表 true 显示图片
    show = Column(String(1), nullable=False, default=1)

    @classmethod
    def save_one(cls, img):
        suffix = img.filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        print('文件名', filename)
        path = os.path.join('static/images', filename)
        print('储存路径', path)
        img.save(path)
        # 获取图片信息
        img_size = Image.open(img).size
        # 图片转码 base64 ， 计算 hash 值，保存\
        is_same_hash, hash_img = cls.img_to_hash(img)
        # img.save(path)
        if is_same_hash is None:
            print('查询结果是 None')
            data = dict(
                file_name= filename,
                origin_name=img.filename,
                width=img_size[0],
                height=img_size[1],
                src=path,
                hash=hash_img
            )
            r = cls.new(data).json()
            # temp_img.save(path)
            print('保存 img', img)
            print('保存 path', path)
        else:
            print('{} 已存在'.format(img.filename))
            os.remove(path)
            r = None
        return r
    @classmethod
    def img_to_hash(cls,img):
        img_info = img.read()
        img_info_len = len(img_info)
        base64_img = base64.encodebytes(img_info)
        # print('{} base64_img'.format(img.filename), base64_img)
        hash_img = hashlib.md5(base64_img).hexdigest()
        # print('{} hash img'.format(img.filename), hash_img[:50])
        # 查找数据库中是否有同样的 hash 值 图片
        is_same_hash = cls.one(hash=hash_img)
        print('{} hash值图片查重结果'.format(img.filename), is_same_hash is not None)
        return is_same_hash, hash_img

