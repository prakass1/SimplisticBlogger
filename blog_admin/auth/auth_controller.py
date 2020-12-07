from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import login_required, current_user, logout_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    return render_template("auth/login.html")

@auth_bp.route("/intrim_login", methods=["GET"])
@login_required
def intrim_login():
    if current_user.changed_pass:
        return redirect(url_for("auth.dashboard"))

    return render_template("auth/login_intrim.html", user = current_user)
    

@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html", user = current_user)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.admin"))
