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

@main.route('/static')
def static():
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.args['file']
    return send_from_directory('static', filename)