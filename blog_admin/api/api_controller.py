from flask import (Blueprint, redirect, url_for, request,
                   flash, abort, send_file, send_from_directory)
import uuid
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user
from urllib import parse
import os
import datetime
from sqlalchemy import exc
import traceback
from common import db
from common.models.users_model import Users
from common.models.images_model import Images
from common.services.users_service import UserService
from blog_admin.posts.service import posts_service

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
        current_dm = str(datetime.datetime.now()).split(".")[0].split(" ")[0].replace("-","")

        if file.filename == "":
            return "error.png"
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                if not os.path.exists(os.environ.get("UPLOAD_FOLDER") + "/" + current_dm):
                    os.makedirs(os.environ.get("UPLOAD_FOLDER") + "/" + current_dm)
                file.save(os.path.normpath(os.path.join(os.environ.get("UPLOAD_FOLDER"),
                                                        current_dm, filename)))
                set_url = "".join("/image/" + current_dm + "/" + file.filename)
                return set_url
            except Exception:
                traceback.print_exc()
                abort(500)
                return "Internal Error, check logs"

@api_bp.route("/image_delete", methods=["POST"])
@login_required
def delete_image():
    try:
        payload = request.get_json()
        image_file = payload["image_file"]
        image_path_list = image_file.split("/")
        blog_post_val = image_path_list[len(image_path_list) - 2]
        image_file_name = image_path_list[len(image_path_list) - 1]
        image_rel_url = "/image" + "/" + blog_post_val + "/" + image_file_name

        #file location removal
        os.remove(os.environ.get("UPLOAD_FOLDER") + "/" + blog_post_val + "/" + image_file_name)
        
        image = Images.query.filter_by(image_url=image_rel_url).first()
        if image:
            #Remove from database
            #database
            db.session.delete(image)
            db.session.commit()

        return "Successfully removed the image file"

    except (FileNotFoundError, exc.SQLAlchemyError) as e:
        traceback.print_exc()
        return "File cannot be delete, check logs !!!"

@api_bp.route("/image/<curr_dm>/<filename>", methods=["GET"])
@login_required
def get_image(curr_dm, filename):
    try:
        dir_abs_path = os.path.dirname(os.path.abspath(os.environ.get("UPLOAD_FOLDER")))
        return send_from_directory(dir_abs_path + "\\" + os.environ.get("UPLOAD_FOLDER") + "\\" + str(curr_dm), filename)
    except FileNotFoundError:
        abort(404)
    

