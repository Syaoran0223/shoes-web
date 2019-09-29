from sqlalchemy import create_engine

# from config.secret import database_password, database, database_port, database_ip
# from config import secret
from config import dev
secret = dev
from app import configured_app
from models.base_model import db
# from models.teacher import Teacher
# from models.picture import Picture as Img
from models.product import Product
# from models.board import Board
# from models.reply import Reply
# from models.topic import Topic
# from models.user import User


def reset_database():
    # url = 'mysql+pymysql://root:{}@localhost:{}/?charset=utf8mb4'.format(
    # # url='mysql+pymysql://root:{}@mysql/?charset=utf8mb4'.format(
    #     database_ip, database_password, database_port)
    url = 'mysql+pymysql://{username}:{password}@{db_addr}:{db_port}/{db_name}'.\
        format(username=secret.db_username, password=secret.db_password,
               db_addr=secret.db_addr, db_name=secret.db_name, db_port=secret.db_port)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(secret.db_name))
        c.execute(
            'CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(secret.db_name))
        c.execute('USE {}'.format(secret.db_name))

    db.metadata.create_all(bind=e)


def generate_fake_date():
    # User.validateSQL()
    shoes1 = dict(
        name='AIR JORDAN 4 RETROSNGLDY',
        shoes_code='BQ0897 006'
    )
    p = Product.addProduct(shoes1)
    print('新增商品', p)
    # form = dict(
    #     username='admin',
    #     password='admin',
    #     token='admin',
    #     avatar='http://thirdwx.qlogo.cn/mmopen/hgXWbMaaqmAj8fAKJJq1nozVgMrm7CfOd7w1W7UleKwFJT2dQbE7W9qRWr04Zra7W1PRQ5fibRZgqr7myOiadx6Q/132'
    # )
    # u = User.register(form)
    # user1 = dict(
    #     username='feng',
    #     password='123456',
    #     token='admin',
    #     avatar='http://cdn.aixifan.com/dotnet/20130418/umeditor/dialogs/emotion/images/ac/02.gif'
    # )
    # u = User.register(user1)
    # print('u', u.json())
    # teahcer1 = dict(
    #     name='73',
    #     avatar='/static/images/avatar-73.png',
    #     job='曼奇立德高级讲师',
    #     introduce='自身游戏原画师/CG艺术家',
    #     type='01'
    # )
    # t = Teacher.new(teahcer1)
    # print('初始化默认教师', t)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
#
