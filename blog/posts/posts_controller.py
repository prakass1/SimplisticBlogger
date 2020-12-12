from flask import Blueprint
from flask import render_template, request, redirect,url_for

posts_bp = Blueprint(
    "posts", __name__)

@posts_bp.route("/", methods=["GET"])
def blog():
    return render_template("blog/index.html")


@posts_bp.route("/post")
def post():
    return render_template("blog/post.html")
