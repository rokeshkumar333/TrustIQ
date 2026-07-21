from flask import Blueprint, request, jsonify
import os
import uuid

from werkzeug.utils import secure_filename

from app.services.upload_service import save_document_details

upload = Blueprint("upload", __name__)

# Upload Folder
UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed Extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload.route("/upload", methods=["POST"])
def upload_file():

    # Check whether file exists
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    file = request.files["file"]

    # Check empty filename
    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Filename is empty"
        }), 400

    # Validate extension
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Only PDF, JPG, JPEG and PNG files are allowed"
        }), 400

    # Original filename (safe)
    original_filename = secure_filename(file.filename)

    # Extract extension
    extension = original_filename.rsplit(".", 1)[1].lower()

    # Generate UUID filename
    stored_filename = f"{uuid.uuid4()}.{extension}"

    # Complete file path
    filepath = os.path.join(UPLOAD_FOLDER, stored_filename)

    # Save file
    file.save(filepath)

    # Save metadata into PostgreSQL
    save_document_details(
        user_id=1,                     # Temporary (JWT integration later)
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=filepath,
        file_type=extension
    )

    return jsonify({
        "success": True,
        "message": "File uploaded successfully",
        "original_filename": original_filename,
        "stored_filename": stored_filename
    }), 200