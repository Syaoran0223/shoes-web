from sqlalchemy import create_engine

from config.secret import database_password, database
from app import configured_app
from models.base_model import db
from models.teacher import Teacher
from models.picture import Picture as Img
# from models.board import Board
# from models.reply import Reply
# from models.topic import Topic
from models.user import User

def reset_database():
    url = 'mysql+pymysql://root:{}@localhost:8806/?charset=utf8mb4'.format(
    # url='mysql+pymysql://root:{}@mysql/?charset=utf8mb4'.format(
        database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(database))
        c.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(database))
        c.execute('USE {}'.format(database))

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='admin',
        password='admin',
        token='admin'
    )
    u = User.register(form)
    print('u', u.json())
    teahcer1 = dict(
        name='73',
        avatar='/static/images/avatar-73.png',
        job='曼奇立德高级讲师',
        introduce='自身游戏原画师/CG艺术家',
        type='01'
    )
    t = Teacher.new(teahcer1)
    print('初始化默认教师', t)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
#
