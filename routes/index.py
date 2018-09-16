import os
import uuid

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
main = Blueprint('index', __name__)

@main.route("/", methods=['GET'])
def index():
    # u = current_user()
    return render_template("index.html")

@main.route('/static/images/<filename>', methods=['GET'])
def image(filename):
    print('filename', filename)
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    return send_from_directory('static/images/', filename)