from flask import Blueprint, jsonify

from app.services.document_service import get_all_documents
from app.utils.auth_middleware import token_required

qr = Blueprint("qr", __name__)


@qr.route("/qr-verification", methods=["GET"])
@token_required
def qr_verification_summary():
    documents = get_all_documents()
    results = []

    for document in documents:
        qr_verification = document.get("qr_verification", {}) if isinstance(document, dict) else {}
        results.append({
            "id": document.get("id") if isinstance(document, dict) else None,
            "original_filename": document.get("original_filename", "") if isinstance(document, dict) else "",
            "verified": qr_verification.get("verified", False),
            "method": qr_verification.get("method", "text-pattern"),
            "message": qr_verification.get("message", "No QR verification data available."),
            "markers": qr_verification.get("markers", []),
        })

    return jsonify({
        "success": True,
        "verifications": results,
    })
