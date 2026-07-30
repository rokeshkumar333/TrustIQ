from flask import Blueprint, jsonify, g

from app.services.classification_service import classify_document
from app.services.document_service import get_all_documents
from app.utils.auth_middleware import token_required

classification = Blueprint("classification", __name__)


@classification.route("/classification", methods=["GET"])
@token_required
def classification_summary():
    documents = get_all_documents()
    classifications = []

    for document in documents:
        fields = document.get("fields", {}) if isinstance(document, dict) else {}
        original_filename = document.get("original_filename", "") if isinstance(document, dict) else ""
        classifications.append({
            "id": document.get("id") if isinstance(document, dict) else None,
            "original_filename": original_filename,
            **classify_document(fields, original_filename),
        })

    return jsonify({
        "success": True,
        "classifications": classifications,
        "user": {
            "id": g.user_id,
            "email": g.user_email,
        },
    })
