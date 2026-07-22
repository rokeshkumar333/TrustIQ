from flask import Blueprint, request, jsonify, g
import os
import uuid
from werkzeug.utils import secure_filename

from app.services.upload_service import save_document_details
from app.services.document_pipeline import process_document
from app.utils.auth_middleware import token_required

upload = Blueprint("upload", __name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload.route("/upload", methods=["POST"])
@token_required
def upload_file():

    # Check file exists
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

    # Secure filename
    original_filename = secure_filename(file.filename)

    # Extension
    extension = original_filename.rsplit(".", 1)[1].lower()

    # UUID filename
    stored_filename = f"{uuid.uuid4()}.{extension}"

    # Save path
    filepath = os.path.join(
        UPLOAD_FOLDER,
        stored_filename
    )

    # Save uploaded file
    file.save(filepath)

    # Default OCR text
    extracted_text = ""

    # Process document
    try:

        if extension == "pdf":

            pipeline_result = process_document(filepath)

            extracted_text = pipeline_result.get(
                "ocr_text",
                ""
            )

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "AI Processing Failed",
            "error": str(e)
        }), 500

    # Save metadata + OCR text
    save_document_details(
        user_id=g.user_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=filepath,
        file_type=extension,
        extracted_text=extracted_text
    )

    return jsonify({
        "success": True,
        "message": "File uploaded successfully",
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "ocr_text": extracted_text
    }), 200