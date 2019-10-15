from sqlalchemy import create_engine

# from config.secret import database_password, database, database_port, database_ip
from config import secret
# from config import dev
# secret = dev
from app import configured_app
from models.base_model import db
# from models.teacher import Teacher
# from models.picture import Picture as Img
from models.product import Product
from models.product_attr import ProductAttr
from models.user import User
from models.batch import Batch
from models.dictMap import DictMap
from models.session import Session
print('数据类型', secret.db_port)


def reset_database():
    # url = 'mysql+pymysql://root:{}@localhost:{}/?charset=utf8mb4'.format(
    # # url='mysql+pymysql://root:{}@mysql/?charset=utf8mb4'.format(
    #     database_ip, database_password, database_port)
    url = 'mysql+pymysql://{username}:{password}@{db_addr}:{db_port}/'.format(username=secret.db_username,
                                                                              password=secret.db_password,
                                                                              db_addr=secret.db_addr,
                                                                              # db_name=secret.db_name,
                                                                              db_port=secret.db_port)
    print('url', url)
    e = create_engine(url, echo=True)
    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(secret.db_name))
        c.execute(
            'CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(secret.db_name))
        c.execute('USE {}'.format(secret.db_name))

    db.metadata.create_all(bind=e)


def generate_fake_date():
    print('测试开始')
    # 增加 类型
    product1 = dict(
        name='AIR JORDAN 11 RETRO',
        code='AR0715 200',
        cover='https://c.static-nike.com/a/images/t_prod_ss/w_960,c_limit,f_auto/c0k2mkpdrvz3caggsm7f/womens-air-jordan-11-neutral-olive-sail-gum-light-brown-release-date.jpg',
        note='橄榄 女款',
    )
    product2 = dict(
        name='AIR JORDAN 1 MID',
        code='AR0715 200',
        cover='https://inews.gtimg.com/newsapp_bt/0/9964332871/1000',
        note='黒曜石 黑白',
    )
    p = Product.add(product1)
    p2 = Product.add(product1)

    Product.add(product2)
    print('p', p.id)
    # 增加子类型
    product1_attr1 = dict(
        bar_code='191888280841',
        size="38.5",
        product_id=p.id
    )
    product1_attr2 = dict(
        bar_code='191888280858',
        size="39",
        product_id=p.id
    )
    ProductAttr.new(product1_attr1)
    ProductAttr.new(product1_attr2)
    p3 = dict(
        bar_code="191888280841"
    )
    p3 = ProductAttr.queryByBarCode(p3)
    print('p3', p3)
    p4 = ProductAttr.all()
    print('p444444444444', p4)
    # 增加用户
    u = dict(
        openid="oACYX0d8qtLPAZ6Mtx0sgBY3AtGw",
        identity=0,
    )
    User.login(u)
    # 增加字典表
   
    d1 = [
        {
            'key': 0,
            'value': '管理员',
            'status': 0,
            'type': 'USER_TYPE',
            'note': '用户权限',
        },
        {
            'key': 1,
            'value': '普通用户',
            'status': 0,
            'type': 'USER_TYPE',
            'note': '用户权限',
        },
        {
            'key': 0,
            'value': '出售中',
            'status': 0,
            'type': 'STOCK_STATUS',
            'note': '出售状态',
        },
        {
            'key': 1,
            'value': '已出售',
            'status': 0,
            'type': 'STOCK_STATUS',
            'note': '出售状态',
        },
        {
            'key': 2,
            'value': '寄售',
            'status': 0,
            'type': 'STOCK_STATUS',
            'note': '出售状态',
        },
        {
            'key': 3,
            'value': '退回中',
            'status': 0,
            'type': 'STOCK_STATUS',
            'note': '出售状态',
        },
        {
            'key': 0,
            'value': '未上传',
            'status': 0,
            'type': 'BATCH_UPLOAD',
            'note': '批次表格导入状态',
        },
        {
            'key': 1,
            'value': '已上传',
            'status': 0,
            'type': 'BATCH_UPLOAD',
            'note': '批次表格导入状态',
        },

    ]
    DictMap.new_by_list_dict(d1)
    # 新增批次
    b1 = dict(
        purchase_time='2019-8-26',
        name='测试',
        proportion=5
    )
    b2 = dict(
        purchase_time='2019-9-1',
        name='批次2',
        proportion=10
    )
    Batch.new(b1)
    Batch.new(b2)

    # # 增加商品
    # s1 = dict(
    #     status=0,
    #     cost=100,
    #     price=1200,
    #     batch='新增的鞋子 2019-9-1',
    #     # express_price=24,
    #     # order_id=1
    #     count=5,
    #     product_id=1
    # )
    # s = Stock.add_by_count(s1)
    # print('s', s)
    # ss = Stock.queryAll()
    # print('查询鞋子结果', ss)
    # p2 = ProductAttr.queryAll()
    # print('p2', p2)
    # product1_attr1()


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
#
