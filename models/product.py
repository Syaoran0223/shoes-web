import hashlib

from sqlalchemy import Column, String, Text, Float
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


class Product(SQLMixin, db.Model):
    __tablename__ = 'Product'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    level 有两个属性 'admin', 'edit'
    """
    name = Column(String(50), nullable=False)
    shoes_code = Column(String(50))
    # bar_code = Column(String(50))
    # password = Column(String(100), nullable=False)
    # avatar = Column(String(200), nullable=False, default='/images/3.jpg')
    # token = Column(String(20), nullable=False, default='edit')

    @staticmethod
    def validateSQL(cls):
        # sql = "select * from user"
        # r = db.session.execute(str)
        r = cls.query.all()
        print('测试语句', r)
        return

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt=secret_key):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def addProduct(cls, form):
        print('form', form)
        # name = form.get('username', '')
        p = cls.new(form)
        return p

    @classmethod
    def querUserFromSession(cls):
        uid = session.get('user_id')
        return cls.one(id=uid)
