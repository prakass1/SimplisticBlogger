from flask import (Blueprint,send_from_directory, request, abort)
import os
from flask_login import login_required
import datetime
from werkzeug.utils import secure_filename
import traceback
from common import db
from common.models.images_model import Images
from sqlalchemy import exc


image_bp = Blueprint("image_api", __name__)

# Allowed files to be uploaded
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_bp.route("/image_upload", methods=["GET", "POST"])
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

@image_bp.route("/image_delete", methods=["POST"])
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

    except (FileNotFoundError, exc.SQLAlchemyError):
        traceback.print_exc()
        return "File cannot be delete, check logs !!!"

@image_bp.route("/image/<curr_dm>/<filename>", methods=["GET"])
def get_image(curr_dm, filename):
    try:
        dir_abs_path = os.path.dirname(os.path.abspath(os.environ.get("UPLOAD_FOLDER")))
        return send_from_directory(dir_abs_path + "\\" + os.environ.get("UPLOAD_FOLDER") + "\\" + str(curr_dm), filename)
    except FileNotFoundError:
        abort(404)
