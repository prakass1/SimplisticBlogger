from flask import (Blueprint, redirect, url_for, request,
                   flash, abort, send_file, send_from_directory)
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user
from urllib import parse
import os
from common import db
from common.models.users_model import Users
from common.services.users_service import UserService

api_bp = Blueprint("api", __name__)

# Allowed files to be uploaded
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Safe url function handy for redirects

def is_safe_url(target):
    ref_url = parse.urlparse(request.host_url)
    test_url = parse.urlparse(parse.urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@api_bp.route("/")
def index():
    return redirect(url_for("auth.admin"))


@api_bp.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    user_name = request.form.get("username")
    password = request.form.get("password")
    user = Users.query.filter_by(user_name=user_name).first()
    next_link = request.args.get("next")
    if not user or not check_password_hash(user.password, password):
        flash("Looks like the provided login credentials are not correct !!!. Please login again")
        return redirect(url_for("auth.admin"))
    # Login the user into flask-login
    login_user(user)

    if not is_safe_url(next_link):
        return abort(400)

    if user.changed_pass:
        return redirect(url_for("auth.dashboard"))

    return redirect(next_link or url_for("auth.intrim_login"))


@api_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    old_pass = request.form.get("old-password")
    new_pass = request.form.get("new-password")

    user = Users.query.filter_by(user_name=current_user.user_name).first()

    if not check_password_hash(user.password, old_pass):
        flash("Looks like the provided old password is wrong. Try again !!!")
        return redirect(url_for("auth.intrim_login"))
    print("Sucess with change_password() call")
    user.password = generate_password_hash(new_pass)
    user.changed_pass = True
    db.session.commit()
    flash("Updated your password, Welcome to the Admin Dashboard")
    return redirect(url_for("auth.dashboard"))


@api_bp.route("/image_upload", methods=["GET", "POST"])
@login_required
def upload_images():
    if request.method == "POST":
        file = request.files["image"]
        blog_title = request.form.get("blog_title")
        blog_title = blog_title.replace(" ", "-")
        print(file.filename, blog_title)
        if file.filename == "":
            return "error.png"
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                if not os.path.exists(os.environ.get("UPLOAD_FOLDER") + "/" + blog_title):
                    os.makedirs(os.environ.get("UPLOAD_FOLDER") + "/" + blog_title)
                file.save(os.path.normpath(os.path.join(os.environ.get("UPLOAD_FOLDER"),
                                                        blog_title, filename)))
                set_url = "".join("/image/" + blog_title + "/" + file.filename)
                return set_url
            except Exception:
                return "There has been an error with the request. Please Check logs !!"


@api_bp.route("/image/<blog_title>/<filename>", methods=["GET"])
@login_required
def get_image(blog_title, filename):
    try:
        dir_abs_path = os.path.dirname(os.path.abspath(os.environ.get("UPLOAD_FOLDER")))
        return send_from_directory(dir_abs_path + "\\" + os.environ.get("UPLOAD_FOLDER") + "\\" + blog_title, filename)
    except FileNotFoundError:
        abort(404)
