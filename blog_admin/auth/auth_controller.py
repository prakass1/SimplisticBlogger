from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import login_required, current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def admin():
    return render_template("auth/login.html")

@auth_bp.route("/intrim_login", methods=["GET"])
def intrim_login():
    print(current_user.name)
    return render_template("auth/login_intrim.html", user = current_user)
