import os
import time
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from sqlalchemy import Column, Integer, String, func, DateTime
import json
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_time = Column(Integer, default=int(time.time()))

    @classmethod
    def sql_to_list(cls, proxy):
        list = []
        for row in proxy:
            print('row.keys', row.keys())
            print('row values', row.values())
            list.append(dict(zip(row.keys(), row.values())))
        return list

    @classmethod
    def sql_to_dict(cls, proxy):
        list = cls.sql_to_list(proxy)
        print('to dict ', list)
        return list[0]

    @classmethod
    def new(cls, form):
        m = cls()
        # print('new before', m)
        for name, value in form.items():
            # print(m, name, value)
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()
        # print('newTest', m)
        return m

    @classmethod
    def new_by_list_dict(cls, list_dict):
        # list_dict   ->  [{},{}]
        ms = []
        for ld in list_dict:
            m = cls()
            for name, value in ld.items():
                setattr(m, name, value)
            ms.append(m)
            db.session.add(m)
        db.session.commit()    
        ms = [m.json() for m in ms]
        return ms

    @classmethod
    def new_by_shoes_excel(cls, list):
        # list -> [{*:*, count: 1}] 根据列表中count数量 循环
        print('form in model', list)
        ms = []
        for form in list:
            length = int(form.get('count'))
            print('form', form)
            print('数量', length)
            for index in range(length):
                # print('ssss', index)
                m = cls()
                for name, value in form.items():
                    setattr(m, name, value)
                db.session.add(m)
                ms.append(m)
                print('m', index, m)

                # list.append(m.json())
                # db.session.add(m)
        db.session.commit()
        ms = [m.json() for m in ms]
        return ms

    @classmethod
    def delete_one(cls, **kwargs):
        print('base delete_one kwargs', kwargs)
        m = cls.one(**kwargs)
        db.session.delete(m)
        db.session.commit()
        print('base delete_one m', m)
        if hasattr(m, 'src') is True:
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
        db.session.commit()
        delete_result = cls.query.filter(cls.id.in_(tuple(ids))).all()
        return delete_result

    @classmethod
    def update(cls, id=None, **kwargs):
        print('update, id', id, )
        print('base update **kwargs', kwargs)
        id = id or kwargs.get('id')
        m = cls.query.filter_by(id=id).first()
        print('m', m)
        for name, value in kwargs.items():
            if name != 'id':
                print('base update name', name, value)
                setattr(m, name, value)

        print('base update_end m', m)
        db.session.add(m)
        db.session.commit()
        r = cls.one(id=id).json()
        return r

    @classmethod
    def all(cls, **kwargs):
        # print('base_model all kwargs', kwargs)
        # if int(kwargs['page_size']) and int(kwargs['page_index']):
        #     page_size = int(kwargs['page_size'])
        #     page_index = int(kwargs['page_index'])
        #     ms = cls.query.filter_by().limit(page_size).offset(
        #         (page_index - 1) * page_size).all()
        # else:
        #     print('没有页数')
        #     ms = cls.query.filter_by().all()
        # print('all sql ', cls, ms)
        ms = cls.query.filter_by().all()
        ms = [m.json() for m in ms]
        filterMap = dict(
            created_time={
                'date_type': "%Y-%m-%d %H:%M:%S",
            },
            updated_time={
                'date_type': "%Y-%m-%d %H:%M:%S",
            },
            purchase_time={
                'date_type': "%Y-%m-%d",
            }
        )
        keyMap = filterMap.keys()
        # 格式化日期
        for m in ms:
            for i in m:
                if i in keyMap and m[i] is not None:
                    # format = '%Y-%m-%d %H:%M:%S'
                    ct = m[i]
                    m[i] = ct.strftime(filterMap[i].get('date_type'))

        total = db.session.query(func.count(cls.id)).scalar()
        r = dict(
            list=ms,
            total=total,
        )
        return r

    @classmethod
    def queryImageByCondition(cls, **kwargs):
        print('base_model all kwargs', kwargs)
        # page_size = int(kwargs['page_size']) or None
        page_size = hasattr(kwargs, 'page_size')
        # print('base_modal queryByCondition page_size', page_size)
        # page_index = int(kwargs['page_index'])
        page_index = hasattr(kwargs, 'page_index')
        title = kwargs['title']
        print(page_size, page_index, title)
        if page_size and page_index:
            page_size = int(kwargs['page_size'])
            page_index = int(kwargs['page_index'])
            print('有页码')
            ms = cls.query.filter(cls.file_name.like('%{}%'.format(title))).limit(page_size).offset(
                (page_index - 1) * page_size).all()
        else:
            print('有标题', title)
            ms = cls.query.filter(
                cls.file_name.like('%{}%'.format(title))).all()
        # 总数量
        count = db.session.query(func.count(cls.id)).scalar()
        ms = [m.json() for m in ms]
        print('搜索结果', ms)
        return ms, count

    @classmethod
    def queryByCondition(cls, **kwargs):
        print('base_model all kwargs', kwargs)
        # page_size = int(kwargs['page_size']) or None
        page_size = hasattr(kwargs, 'page_size')
        # print('base_modal queryByCondition page_size', page_size)
        # page_index = int(kwargs['page_index'])
        page_index = hasattr(kwargs, 'page_index')
        title = kwargs['title']
        print(page_size, page_index, title)
        if page_size and page_index:
            page_size = int(kwargs['page_size'])
            page_index = int(kwargs['page_index'])
            print('有页码')
            ms = cls.query.filter(cls.name.like('%{}%'.format(title))).limit(page_size).offset(
                (page_index - 1) * page_size).all()
        else:
            print('有标题', title)
            ms = cls.query.filter(cls.name.like('%{}%'.format(title))).all()
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

    def default(self, obj):
        print('执行了的defalut')
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

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

    def column_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']

    # def sqlJson(self):

    # def json(self):
    #     dict = self.__dict__
    #     dict.pop('_sa_instance_state')
    #     return dict


class SimpleUser(SQLMixin, db.Model):
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


if __name__ == '__main__':
    # db.create_all()
    form = dict(
        username='feng',
        password='123',
    )
    u = SimpleUser.new(form)
    print(u)
    u = SimpleUser.one(username='123')
    print(u)
