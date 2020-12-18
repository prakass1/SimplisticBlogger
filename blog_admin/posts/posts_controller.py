from flask import Blueprint, render_template
from flask_login import login_required, current_user
from common.services import posts_service

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/overview.html")
@login_required
def dash_overview():
    return render_template("dashboard/overview.html", user=current_user)


@posts_bp.route("/posts.html")
@login_required
def dash_posts():
    #load all posts
    posts = posts_service.PostService.get_all_posts(order_by=True, is_admin=True)
    return render_template("dashboard/posts.html", user=current_user, posts=posts)


@posts_bp.route("/add_post.html")
@login_required
def add_post():
    return render_template("dashboard/add_post.html", user=current_user)

@posts_bp.route("/edit_post.html/<post_title>")
@login_required
def edit_post(post_title):
    print(post_title)
    post = posts_service.PostService.get_post_by_title(post_title, is_admin=True)
    tags = posts_service.PostService.get_tags_for_post(post)
    print(tags)
    return render_template("dashboard/edit_post.html", user=current_user, post=post, tags=tags)
