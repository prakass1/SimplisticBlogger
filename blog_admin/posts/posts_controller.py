from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from common import db
from blog_admin.posts.service import posts_service
from bs4 import BeautifulSoup

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/overview.html")
@login_required
def dash_overview():
    return render_template("dashboard/overview.html", user=current_user)


@posts_bp.route("/posts.html")
@login_required
def dash_posts():
    #load all posts
    posts = posts_service.PostService.get_all_posts()
    return render_template("dashboard/posts.html", user=current_user, posts=posts)


@posts_bp.route("/add_post.html")
@login_required
def add_post():
    return render_template("dashboard/add_post.html", user=current_user)

@posts_bp.route("/edit_post.html/<post_title>")
@login_required
def edit_post(post_title):
    print(post_title)
    post = posts_service.PostService.get_post_by_title(post_title)
    return render_template("dashboard/edit_post.html", user=current_user, post=post)


@posts_bp.route("/post", methods=["POST"])
@login_required
def add():
    request_body = request.get_json()
    blog_title = request_body["blog_title"]
    blog_content = request_body["blog_content"]
    blog_author = request_body["blog_author"]

    # Parse the image url and store it for the purposes of logging
    html_parsed = BeautifulSoup(blog_content, "html.parser")
    img_list = [image["src"] for image in html_parsed.find_all("img")]
    print(img_list)

    # Call the post service to add the post
    p_service_obj = posts_service.PostService()
    rc = p_service_obj.add_post(blog_title, blog_author, blog_content, current_user, img_list)
    if rc:
        data_resp = {"redirect_uri": url_for("posts.dash_posts"), "message": "Successfully inserted the post !!"}
        return jsonify(data_resp)
    return "There has been some error while inserting the post. Check Logs and retry posting again"

@posts_bp.route("/post", methods=["PUT"])
@login_required
def edit():
    request_body = request.get_json()
    blog_title = request_body["blog_title"]
    old_title = request_body["old_title"]
    blog_content = request_body["blog_content"]

    # Parse the image url and store it for the purposes of logging
    html_parsed = BeautifulSoup(blog_content, "html.parser")
    new_img_list = [image["src"] for image in html_parsed.find_all("img")]

    # Call the post service to add the post
    post = posts_service.PostService.get_post_by_title(old_title)
    if post:
        p_obj = posts_service.PostService()
        rc = p_obj.edit_post(post, blog_title, blog_content, new_img_list)
        if rc:
            return "Successfully edited the blog content"
        return "Could not edit the content of blog, check logs"
    else:
        return "No such post to edit"

@posts_bp.route("/post", methods=["DELETE"])
@login_required
def delete():
    request_body = request.get_json()
    blog_title = request_body["blog_title"]

    # Call the post service to add the post
    post = posts_service.PostService.get_post_by_title(blog_title)
    if post:
        p_obj = posts_service.PostService()
        rc = p_obj.delete_post(post)
        if rc:
            flash("Successfully deleted the blog")
            return redirect("posts.dash_posts")
        flash("Could not delete the content of blog, check logs")
        return redirect("posts.dash_posts")
    else:
        flash("No such post to delete, must be a hack !!!")
        return redirect("posts.dash_posts")
