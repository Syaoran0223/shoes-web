import os
import time
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func, DateTime

db = SQLAlchemy()


class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_time = Column(Integer, default=int(time.time()))

    @classmethod
    def new(cls, form):
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

        return m

    @classmethod
    def delete_one(cls, **kwargs):
        m = cls.one(**kwargs)
        db.session.delete(m)
        db.session.commit()
        delete_path = m.src
        if (os.path.exists(delete_path)):
            os.remove(delete_path)
        else:
            print('delete_one', '文件不存在')
        m = cls.one(**kwargs)
        return m

    @classmethod
    def delete_by_ids(cls, ids):
        ms = cls.query.filter(cls.id.in_(tuple(ids))).all()
        for m in ms:
            m = cls.one(id=m.id)
            db.session.delete(m)
            os.remove(m.src)
        db.session.commit()
        delete_result = cls.query.filter(cls.id.in_(tuple(ids))).all()
        return delete_result

    @classmethod
    def update(cls, id, **kwargs):
        print('update, id', id, )
        print('**kwargs', kwargs)
        # u.username = 'test'
        # db.session.add(u)
        # db.session.commit()
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()
        r = cls.one(id=id).json()
        return r

    @classmethod
    def all(cls, **kwargs):
        print('base_model all kwargs', kwargs)
        page_size = int(kwargs['page_size'])
        page_index = int(kwargs['page_index'])
        if page_size and page_index :
            ms = cls.query.filter_by().limit(page_size).offset((page_index - 1) * page_size).all()
        else:
            print('没有页数')
            ms = cls.query.filter_by().all()
        print('all sql ', cls, ms)
        count = db.session.query(func.count(cls.id)).scalar()

        return ms, count

    @classmethod
    def queryByCondition(cls, **kwargs):
        print('base_model all kwargs', kwargs)
        page_size = int(kwargs['page_size'])
        page_index = int(kwargs['page_index'])
        title = kwargs['title']
        print(page_size, page_index, title)
        if page_size and page_index:
            print('有页码')
            ms = cls.query.filter(cls.file_name.like('%{}%'.format(title))).limit(page_size).offset(
                (page_index - 1) * page_size).all()
        else:
            print('有标题', title)
            ms = cls.query.filter(cls.file_name.like('%{}%'.format(title))).all()
        # 总数量
        count = db.session.query(func.count(cls.id)).scalar()
        ms = [m.json() for m in ms]
        print('搜索结果', ms)
        return ms, count
    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        print('one cls', cls, ms)
        return ms

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        不明白就看书或者 搜
        """
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        d = dict()
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d
    # def sqlJson(self):

    # def json(self):
    #     dict = self.__dict__
    #     dict.pop('_sa_instance_state')
    #     return dict


class SimpleUser(SQLMixin, db.Model):
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


if __name__ == '__main__':
    db.create_all()
    form = dict(
        username='feng',
        password='123',
    )
    u = SimpleUser.new(form)
    print(u)
    u = SimpleUser.one(username='123')
    print(u)
