import os
import requests
from flask import Blueprint, request, jsonify
from common.services.posts_service import PostService
from common.services import comments_service

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
    is_admin = False
    post_data = PostService().get_post_by_title(blog_title)

    if len(post_data) > 0:
        # Ideally there must be a post
        comments_service_obj = comments_service.CommentService()
        # Verify recaptcha else do not add the comment...
        if verify_recaptcha(g_recaptcha)["success"]:
            print("Recaptcha is verified, is human")
            if author_email == os.environ.get("EMAIL"):
                is_admin=True
            
            if comments_service_obj.add_comment(author_name, author_email, author_comment, post_data[0], is_admin=is_admin):   
                if is_admin:
                    c_status = comments_service.CommentService.send_email(author_comment, author_name, post_data[0])
                    if c_status:
                        #Admin and it is a reply
                        return "Your comment is posted and notification sent to the original commenter"
                    
                    #Admin but not reply
                    return "Your comment is posted"
                
                # Commented but not admin
                return "Your comment is posted and is under moderation"
            
            #Internal error
            return "There has been an error while posting the comment, try after sometime..."
        #recaptcha failed
        return "Cannot comment this request"


@comments_bp.route("/api/comment", methods=["PUT"])
def approve_comment():
    request_body = request.get_json()
    comment_ref_id = request_body["comment_ref_id"]
    comment_status = request_body["comment_status"]
    if comment_ref_id and comment_status:
        #Edit to approve or reject comment
        comment_serv_obj = comments_service.CommentService()
        resp = comment_serv_obj.edit_comment(comment_ref_id.split("-")[1], comment_status)
        print(resp)
        return jsonify(resp)
    else:
        data_resp = {"resp":False, "message": "Payload passed is empty"}
        return jsonify(data_resp)
