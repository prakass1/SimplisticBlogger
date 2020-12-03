from flask import Blueprint, render_template, request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/administrator")
def admin():
    return render_template("auth/login.html")