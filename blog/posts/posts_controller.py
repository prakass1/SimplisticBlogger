from flask import Blueprint
from flask import render_template, request, redirect, url_for
from common.services.posts_service import PostService
from blog import resp

import os

posts_bp = Blueprint(
    "posts", __name__)


@posts_bp.route("/", methods=["GET"])
def blog():
    post_obj = PostService()
    limit = os.environ.get("page_init_limit")
    posts = post_obj.get_all_posts()
    if posts:
        posts_data = posts[:limit]
    else:
        posts_data = False
    return render_template("blog/index.html", posts_data=posts_data, resp = resp)

@posts_bp.route("/post/<blog_title>")
def get_post_title(blog_title):
    post = PostService().get_post_by_title(blog_title)
    if post:
        post_data = post
    else:
        post_data = False

    return render_template("blog/post.html", post_data=post_data, resp=resp)
