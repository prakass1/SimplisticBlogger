from flask import Blueprint, render_template
from flask_login import login_required, current_user
from common.services import comments_service

comments_bp = Blueprint("comments", __name__)
#count_comments = comments_service.CommentService.get_comment_count(is_admin=True)


@comments_bp.route("/comments.html")
@login_required
def dash_comments():
    #load all comments under_moderation
    comments = comments_service.CommentService.get_comments(is_admin=True)
    return render_template("dashboard/comments_moderation.html", comments=comments)
