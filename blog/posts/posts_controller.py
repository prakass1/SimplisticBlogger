import os
from flask import Blueprint, render_template, request, redirect, url_for
from common.services.posts_service import PostService
from common.services import tags_service, comments_service
from blog import resp
from blog import cache
from blog.posts.service import posts_blog_service

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
        post_len = 0

    return render_template("blog/index.html",
                           posts_data=posts_data,
                           tags_count=tags_service.get_tags_count(),
                           resp=resp, prev_limit=prev_limit,
                           post_len=post_len)


@posts_bp.route("/post/<blog_title>")
def get_post_title(blog_title):
    post_data = PostService().get_post_by_title(blog_title)
    # load all comments under_moderation
    comments = comments_service.CommentService.get_comments(
        post_db_obj=post_data[0], is_admin=False)
    print(comments)
    if len(post_data) > 0:
        data_resp = {"post_data": post_data[0],
                     "tags": post_data[1], "comments": comments}
    else:
        data_resp = {"post_data": False, "tags": False, "comments": comments}

    return render_template("blog/post.html", data_resp=data_resp, resp=resp, site_key=os.environ.get("RECAPTCHA_SITE_KEY"))


@posts_bp.route("/post/category/<tag>")
def get_post_tag(tag):
    prev_limit = request.args.get("prev_limit")
    posts = tags_service.get_post_tags(tag)
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
        return {"posts_resp": posts_serialized,
                "posts_html_reponse": posts_blog_service.get_posts_html_resp(posts_serialized, len(posts_data), new_limit),
                "prev_limit": new_limit,
                "load_more": True,
                "post_len": post_len}
    else:
        return redirect(url_for("posts.blog"))

    return render_template("blog/index.html",
                           posts_data=posts_data,tags_count=tags_service.get_tags_count(), resp=resp, prev_limit=prev_limit, post_len=post_len)
