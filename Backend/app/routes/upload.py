from flask import Blueprint, request, jsonify, g
import os
import uuid
from werkzeug.utils import secure_filename

from app.services.upload_service import save_document_details
from app.utils.auth_middleware import token_required

upload = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload.route("/upload", methods=["POST"])
@token_required
def upload_file():

    try:

        # Check file exists
        if "file" not in request.files:
            return jsonify({
                "success": False,
                "message": "No file selected"
            }), 400

        file = request.files["file"]

        # Empty filename
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

        # Original filename
        original_filename = secure_filename(file.filename)

        # Extension
        extension = original_filename.rsplit(".", 1)[1].lower()

        # UUID filename
        stored_filename = f"{uuid.uuid4()}.{extension}"

        # File path
        filepath = os.path.join(
            UPLOAD_FOLDER,
            stored_filename
        )

        # Save uploaded file
        file.save(filepath)

        # Default values
        extracted_text = ""
        fields = {}
        trust_score = 0
        status = "Not Processed"
        qr_verification = {}

        # Run AI Pipeline only for PDF
        if extension == "pdf":
            from app.services.document_pipeline import process_document

            pipeline_result = process_document(filepath)

            extracted_text = pipeline_result.get(
                "ocr_text",
                ""
            )

            fields = pipeline_result.get(
                "fields",
                {}
            )

            trust_score = pipeline_result.get(
                "trust_score",
                0
            )

            status = pipeline_result.get(
                "status",
                "Unknown"
            )

            qr_verification = pipeline_result.get(
                "qr_verification",
                {}
            )

        # Save into PostgreSQL
        save_document_details(
            user_id=g.user_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=filepath,
            file_type=extension,
            extracted_text=extracted_text,
            trust_score=trust_score,
            status=status,
            fields=fields,
            qr_verification=qr_verification,
        )

        return jsonify({

            "success": True,

            "message": "File uploaded successfully",

            "original_filename": original_filename,

            "stored_filename": stored_filename,

            "ocr_text": extracted_text,

            "fields": fields,

            "trust_score": trust_score,

            "status": status,

            "qr_verification": qr_verification

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500