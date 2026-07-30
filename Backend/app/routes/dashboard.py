from flask import Blueprint, jsonify, g

from app.services.dashboard_service import build_dashboard_summary
from app.services.document_service import get_all_documents
from app.utils.auth_middleware import token_required


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard", methods=["GET"])
@token_required
def dashboard_summary():
    documents = get_all_documents()
    summary = build_dashboard_summary(documents)

    return jsonify({
        "success": True,
        "summary": summary,
        "documents": documents[:5],
        "user": {
            "id": g.user_id,
            "email": g.user_email,
        },
    })
