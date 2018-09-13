from flask import Flask
# 跨域
from flask_cors import CORS

from models.base_model import db
from config import secret
from routes.index import main as index_routes
from routes.user import main as user_routes

# from routes.topic import main as topic_routes
# from routes.reply import main as reply_routes
# from routes.board import main as board_routes
# from routes.message import main as mail_routes, mail

def configured_app():
    app = Flask(__name__)
    CORS(app)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = secret.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        secret.database_password,
        secret.database
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    register_routes(app)
    return app

def register_routes(app):
    app.register_blueprint(user_routes, url_prefix='/user')

# 运行代码
if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['JSON_AS_ASCII'] = False
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
        threaded=True,
    )
    app.run(**config)
