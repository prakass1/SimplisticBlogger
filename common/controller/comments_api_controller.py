import os
import requests
from flask import Blueprint,render_template, request, redirect, url_for
from common.services.posts_service import PostService
from common.services import posts_service,comments_service
from blog import cache

comments_bp = Blueprint(
    "comments_api_bp", __name__)


def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {'secret':os.environ.get("RECAPTCHA_SITE_SECRET"),'response':recaptcha_response} 
    response = requests.post(url, data=payload)
    return response.json()


@comments_bp.route("/api/comment", methods=["POST"])
def add_comment():
    request_body = request.get_json()
    author_name = request_body["author_name"]
    author_email = request_body["author_email"]
    author_comment = request_body["author_comment"]
    blog_title = request_body["blog_title"]
    g_recaptcha = request_body["g_recaptcha"]

    post_data = PostService().get_post_by_title(blog_title)

    if len(post_data) > 0:
        # Ideally there must be a post
        comments_service_obj = comments_service.CommentService()
        # Verify recaptcha else do not add the comment...
        if verify_recaptcha(g_recaptcha)["success"]:
            print("Recaptcha is verified, is human")
            if comments_service_obj.add_comment(author_name, author_email, author_comment, post_data[0]):
                return "Your comment is posted and is under moderation"
            return "There has been an error while posting the comment, try after sometime..."
        return "Cannot comment this request"


@comments_bp.route("/api/comment", methods=["PUT"])
def approve_comment():
    request_body = request.get_json()
    comment_ref_id = request_body["comment_ref_id"]
    comment_status = request_body["comment_status"]
    if comment_ref_id and comment_status:
        #Edit to approve or reject comment
        comment_serv_obj = comments_service.CommentService()
        resp = comment_serv_obj.edit_comment(comment_ref_id, comment_status)
        if resp:
            return "Success"
        return "Failed"
    else:
        return "Failed"