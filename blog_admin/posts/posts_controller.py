from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import login_required, current_user

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/overview")
@login_required
def dash_overview():
    return render_template("dashboard/overview.html", user=current_user)

@posts_bp.route("/posts")
@login_required
def dash_posts():
    return render_template("dashboard/posts.html", user=current_user)

@posts_bp.route("/add_post")
@login_required
def add_post():
    return render_template("dashboard/add_post.html", user=current_user)