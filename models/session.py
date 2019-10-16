# import time
# import pymysql
# import calendar
#
# # from models import Model
# from utils import log
# import datetime
#
# from sqlalchemy import Column, String, Text, Integer, DateTime
# from config.secret import secret_key
# from models.base_model import SQLMixin, db
# from models.res import Res
#
#
# class Session(SQLMixin, db.Model):
#     __tablename__ = 'session'
#
#     """
#     Session 是用来保存 session 的 model
#     """
#     session_id = Column(String(100))
#     user_id = Column(Integer)
#     expired_time = Column(DateTime, default=datetime.datetime.utcnow)
#     # updated_time = Column(DateTime, default=)
#
#     #
#     # sql_create = '''
#     #      CREATE TABLE `session` (
#     #         `id` int(0) NOT NULL AUTO_INCREMENT,
#     #         `session_id` VARCHAR (16) NULL,
#     #         `user_id` int(0) NULL,
#     #         `expired_time` varchar(30) NULL,
#     #         PRIMARY KEY (`id`)
#     #      )'''
#
#     @classmethod
#     def add(cls, form):
#         form = dict(
#             user_id=form.get('id'),
#             session_id=form.get('openid'),
#             expired=datetime.datetime.utcnow()
#         )
#         s = cls.one(session_id = form.get('session_id'))
#         print('查找的 session', s)
#         if s is None:
#             s = cls.new(form)
#             print('新增的session', s)
#
#         return s
#
#     # def __init__(self, form):
#     #     super().__init__(form)
#     #     self.session_id = form.get('session_id', '')
#     #     self.user_id = form.get('user_id', -1)
#     #     self.expired_time = form.get('expired_time', time.time() + 3600)
#
#     def expired(self):
#         now = datetime.datetime.utcnow()
#         print('当前时间', now)
#         print('时间截止', self.expired_time)
#         result = self.expired_time.__sub__(now).seconds > 0
#         print('比较比较比较比较比较比较比较比较比较比较比较', result)
#         print('self', self)
#         # result = (self.expired_time - now).seconds
#         # log('expired', result, self.expired_time, now)
#         return result
#
#
# def test():
#     form = dict(
#         session_id="sgs25l2gg5jgsjs4",
#         user_id=2,
#         expired_time=1534272313.0033321
#     )
#     sid = form.get('session_id')
#     print('测试用 session id', sid)
#     s = Session.new(form)
#     print('s', s)
#     s1 = Session.one(session_id=sid)
#     print('查找结果', s1)
#
#
# if __name__ == '__main__':
#     # recreate_database()
#     Session.init_connection()
#     test()
