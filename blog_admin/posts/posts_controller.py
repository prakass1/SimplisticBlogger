from flask import Blueprint, render_template
from flask_login import login_required, current_user
from common.services import posts_service, comments_service

posts_bp = Blueprint("posts", __name__)

# Count the comments
#count_comments = comments_service.CommentService.get_comment_count(is_admin=True)


@posts_bp.route("/overview.html")
@login_required
def dash_overview():
    return render_template("dashboard/overview.html")


@posts_bp.route("/posts.html")
@login_required
def dash_posts():
    #load all posts
    posts = posts_service.PostService.get_all_posts(order_by=True, is_admin=True)
    return render_template("dashboard/posts.html", posts=posts)


@posts_bp.route("/add_post.html")
@login_required
def add_post():
    return render_template("dashboard/add_post.html")

@posts_bp.route("/edit_post.html/<post_title>")
@login_required
def edit_post(post_title):
    post_data = posts_service.PostService.get_post_by_title(post_title, is_admin=True)
    if len(post_data) > 0:
        data_resp = {"post_data": post_data[0], "tags": posts_service.PostService.serialize_tags(post_data[1])}
    else:
        data_resp = {"post_data": False, "tags": False}

    return render_template("dashboard/edit_post.html", data_resp=data_resp)
