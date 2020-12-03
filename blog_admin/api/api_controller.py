from flask import Blueprint, redirect, url_for

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def index():
    return redirect(url_for("auth.admin"))

@api_bp.route("/login", methods = ["GET", "POST"])
def login():
    return "You have entered here"