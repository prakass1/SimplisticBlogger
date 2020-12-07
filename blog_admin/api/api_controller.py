from flask import Blueprint, redirect, url_for, request, flash, abort
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required
from urllib import parse
from blog_admin.auth.model.users_model import Users

api_bp = Blueprint("api", __name__)

#### Safe url function handy for redirects

def is_safe_url(target):
    ref_url = parse.urlparse(request.host_url)
    test_url = parse.urlparse(parse.urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@api_bp.route("/")
def index():
    return redirect(url_for("auth.admin"))

@api_bp.route("/login", methods = ["POST"])
def login():
    user_name = request.form.get("username")
    password = request.form.get("password")
    user = Users.query.filter_by(user_name=user_name).first()
    next_link = request.args.get("next")
    if not user or not check_password_hash(user.password, password):
        flash("Looks like the provided login credentials are not correct !!!. Please login again")
        return redirect(url_for("auth.admin"))
    # Login the user into flask-login
    bool_val = login_user(user)
    print(bool_val)
    if not is_safe_url(next_link):
        return abort(400)

    return redirect(next_link or url_for("auth.intrim_login"))

@api_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    old_pass = request.form.get("old-password")
    new_pass = request.form.get("new-password")
    print(old_pass, new_pass)
    return "Came here!! to change the existing password"
