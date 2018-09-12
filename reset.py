from sqlalchemy import create_engine

from config.secret import database_password
from app import configured_app
from models.base_model import db
# from models.board import Board
# from models.reply import Reply
# from models.topic import Topic
from models.user import User

def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS magic')
        c.execute('CREATE DATABASE magic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE magic')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='admin',
        password='admin',
    )
    u = User.register(form)
    print('u', u.json())


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
#