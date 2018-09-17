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
    hash = Column(String(100), nullable=True, default='')
    # 1 代表 true 显示图片
    show = Column(String(1), nullable=False, default=1)

    @classmethod
    def save_one(cls, img):
        suffix = img.filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        path = os.path.join('static/images', filename)
        print('file_path', path)
        # 获取图片信息
        img.save(path)
        img_size = Image.open(img).size
        # 图片转码 base64 ， 计算 hash 值，保存\
        print('img.read len', img.read())
        img_info = img.read()
        img_info_len = len(img_info)
        img_info_lenx = img_info_len - (img_info_len % 4 if img_info_len %4 else 4)
        base64_img = base64.decodestring(img_info[:img_info_lenx])

        # print('缺失长度', missing_padding)
        # if missing_padding:
        #     base64_img = base64_img + b'=' * missing_padding
        print('base64_img', base64_img)
        hash_img = hashlib.md5(base64_img).hexdigest()
        print('hash img', hash_img[:50])
        # 查找数据库中是否有同样的 hash 值 图片
        is_same_hash = cls.one(hash=hash_img)
        print('hash值图片查重结果', is_same_hash is None)
        if is_same_hash is None:
            print('查询结果是 None')
            data = dict(
                file_name=filename,
                # origin_name=img.filename,
                width=img_size[0],
                height=img_size[1],
                src=path,
                hash=hash_img
            )
            r = cls.new(data).json()
            # print('Image save_one', r)
        else:
            print('save one hash is None')
            r = None
        return r
