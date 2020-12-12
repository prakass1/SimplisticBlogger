from flask import redirect, url_for, render_template
from flask import Blueprint

api_bp = Blueprint("api", __name__)

@api_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for('posts.blog'))