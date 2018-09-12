import os
import uuid

from utils import log
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory,
    jsonify
)
from routes import cors
from models.user import User
from models.res import Res
main = Blueprint('user', __name__)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    u = User.register(form)
    print('注册', u)    
    return jsonify(u)

@main.route("/login", methods=['POST'])
def login():
    form = request.json
    print('form', form)
    u = User.validate_login(form)    
    r = Res.success(u.json())    
    return jsonify(r)
