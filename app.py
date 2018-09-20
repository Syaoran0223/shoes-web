# 基本配置
from config.base import host, port
from flask import Flask
# 跨域
from flask_cors import CORS
from models.base_model import db
from config import secret
from routes.index import main as index_routes
from routes.user import main as user_routes
from routes.image import main as image
from routes.teacher import main as teacher_routes

def configured_app():
    app = Flask(__name__, static_folder='')
    # app = Flask(__name__, static_folder='templates/static', static_url_path='templates/static')
    # app._static_folder = './template/static'
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
    app.register_blueprint(index_routes)
    app.register_blueprint(user_routes, url_prefix='/api/user')
    app.register_blueprint(image, url_prefix='/api/image')
    app.register_blueprint(teacher_routes, url_prefix='/api/teacher')

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
        host=host,
        port=port,
        threaded=True,
    )
    app.run(**config)
