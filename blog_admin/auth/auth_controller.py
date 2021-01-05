from flask import Blueprint, render_template, request, redirect,url_for, current_app
from flask_login import login_required, current_user, logout_user
from common.services import comments_service

auth_bp = Blueprint("auth", __name__)

@current_app.context_processor
def inject_data():
    count_comments = comments_service.CommentService.get_comment_count(is_admin=True)
    return dict(user=current_user, no_comments=count_comments)

@auth_bp.route("/", methods=["GET"])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for("posts.dash_posts"))

    return render_template("auth/login.html")

@auth_bp.route("/intrim_login", methods=["GET"])
@login_required
def intrim_login():
    if current_user.changed_pass:
        return redirect(url_for("posts.dash_posts"))

    return render_template("auth/login_intrim.html")

@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.admin"))
