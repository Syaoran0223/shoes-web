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


class User(SQLMixin, db.Model):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    level 有两个属性 'admin', 'edit'
    """
    username = Column(String(50))
    password = Column(String(100))
    avatar = Column(String(200))
    token = Column(String(20))
    openid = Column(String(100), nullable=False)
    unionid = Column(String(100))
    session_key = Column(String(100))
    identity = Column(Integer, default=1)

    @classmethod
    def login(cls, form):
        # openid =
        print('form', form.get('openid'))
        r = cls.one(openid=form.get('openid'))
        if r is None:
            r = cls.new(form)
            print('没有用户 新增', r)
        else:
            print('查询到用户', r)
        # 返回部分字段
        r = r.json()
        return r

    @staticmethod
    def validateSQL():
        sql = "select * from user"
        r = db.session.execute(str)
        return

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt=secret_key):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)

    @classmethod
    def querUserFromSession(cls):
        uid = session.get('user_id')
        return cls.one(id=uid)
