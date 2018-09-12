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

@main.route("/")
def index():
    # u = current_user()
    return render_template("index.html")