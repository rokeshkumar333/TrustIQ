from flask import Blueprint, request, jsonify
import os

upload = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Filename is empty"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Invalid file type"
        }), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    return jsonify({
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }), 200