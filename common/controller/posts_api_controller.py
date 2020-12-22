from flask import Blueprint, request, jsonify, url_for
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
from common.services import posts_service


posts_api_bp = Blueprint("posts_api_bp", __name__)


@posts_api_bp.route("/post", methods=["POST"])
@login_required
def add():
    request_body = request.get_json()
    blog_title = request_body["blog_title"]
    blog_content = request_body["blog_content"]
    blog_author = request_body["blog_author"]
    blog_tags_list = request_body["blog_tags"]

    if len(blog_tags_list) == 0:
        blog_tags_list.append("uncategorized")

    # Parse the image url and store it for the purposes of logging
    html_parsed = BeautifulSoup(blog_content, "html.parser")
    img_list = [image["src"] for image in html_parsed.find_all("img")]
    print(img_list)

    # Call the post service to add the post
    p_service_obj = posts_service.PostService()
    rc = p_service_obj.add_post(blog_title, blog_author, blog_content, current_user, img_list, blog_tags_list)
    if rc:
        data_resp = {"redirect_uri": url_for("posts.dash_posts"), "message": "Successfully inserted the post !!"}
        return jsonify(data_resp)
    return "There has been some error while inserting the post. Check Logs and retry posting again"

@posts_api_bp.route("/post", methods=["PUT"])
@login_required
def edit():
    request_body = request.get_json()
    blog_title = request_body["blog_title"]
    old_title = request_body["old_title"]
    blog_content = request_body["blog_content"]
    blog_tags_list = request_body["blog_tags"]

    if len(blog_tags_list) == 0:
        blog_tags_list.append("uncategorized")


    # Parse the image url and store it for the purposes of logging
    html_parsed = BeautifulSoup(blog_content, "html.parser")
    new_img_list = [image["src"] for image in html_parsed.find_all("img")]

    # Call the post service to add the post
    post_data = posts_service.PostService.get_post_by_title(old_title, is_admin=True)
    if len(post_data) > 0:
        p_obj = posts_service.PostService()
        post = post_data[0]
        tags = post_data[1]
        rc = p_obj.edit_post(post,tags, blog_title, blog_content, new_img_list, blog_tags_list)
        if rc:
            return "Successfully edited the blog content"
        return "Could not edit the content of blog, check logs"
    else:
        return "No such post to edit"

@posts_api_bp.route("/post", methods=["DELETE"])
@login_required
def delete():
    request_body = request.get_json()
    blog_title = request_body["blog_title"]

    # Call the post service to add the post
    post_data = posts_service.PostService.get_post_by_title(blog_title, is_admin=True)
    if len(post_data) > 0:
        p_obj = posts_service.PostService()
        rc = p_obj.delete_post(post_data[0], post_data[1])
        if rc:
            return "Successfully deleted the blog"
        return "Could not delete the content of blog, check logs"

    else:
        return "No such post to delete, must be a hack !!!"

# @posts_api_bp.route("/post", methods=["GET"])
# @login_required
# def get_n_posts():
#     limit = request.params.get("limit")
#     posts = posts_service.PostService.get_all_posts()
    
#     if posts:
#         return posts[:limit]
#     else:
#         return False

# @posts_api_bp.route("/post/<blog_title>", methods=["GET"])
# def get_title_post(blog_title):
#     # Call the post service to add the post
#     post = posts_service.PostService.get_post_by_title(blog_title)
#     if post:
#         return post
#     else:
#         return False
