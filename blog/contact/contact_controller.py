from flask import Blueprint, render_template
from blog import resp

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact")
def contact():
    return render_template("blog/contact.html", resp=resp)