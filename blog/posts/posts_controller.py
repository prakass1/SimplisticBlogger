from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from common.services.posts_service import PostService
from blog import resp
from blog import cache
from blog.posts.service import posts_blog_service
import os

posts_bp = Blueprint(
    "posts", __name__)


@posts_bp.route("/", methods=["GET"])
def blog():
    post_obj = PostService()
    prev_limit = request.args.get("prev_limit")
    posts = post_obj.get_all_posts(order_by=True)
    print(cache.get("all-posts-ordered"))
    if not prev_limit and posts:
        post_len = len(posts)
        prev_limit = os.environ.get("post_init_limit")
        posts_data = posts[:int(prev_limit)]
    elif prev_limit and posts:
        post_len = len(posts)
        new_limit = int(prev_limit) + int(os.environ.get("post_init_limit"))
        posts_data = posts[int(prev_limit):new_limit]
        posts_serialized = [posts_blog_service.serialize(
            post) for post in posts_data]
        print(cache.get("more_posts"))
        return {"posts_resp": posts_serialized,
        "posts_html_reponse": posts_blog_service.get_posts_html_resp(posts_serialized, len(posts_data), new_limit),
                "prev_limit": new_limit,
                "load_more": True,
                "post_len": post_len}
    else:
        posts_data = False
    return render_template("blog/index.html",
                           posts_data=posts_data, resp=resp, prev_limit=prev_limit, post_len=post_len)


@posts_bp.route("/post/<blog_title>")
def get_post_title(blog_title):
    post = PostService().get_post_by_title(blog_title)
    if post:
        post_data = post
    else:
        post_data = False

    return render_template("blog/post.html", post_data=post_data, resp=resp)
