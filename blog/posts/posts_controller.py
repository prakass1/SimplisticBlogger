from flask import Blueprint
from flask import render_template, request

posts_bp = Blueprint(
    "posts", __name__)

@posts_bp.route("/", methods=["GET"])
def index():
    return render_template("blog/index.html")


@posts_bp.route("/post")
def post():
    return render_template("blog/post.html")
