from flask import Blueprint, jsonify, g

from app.services.analytics_service import build_analytics_summary
from app.services.document_service import get_all_documents
from app.utils.auth_middleware import token_required

analytics = Blueprint("analytics", __name__)


@analytics.route("/analytics", methods=["GET"])
@token_required
def analytics_summary():
    documents = get_all_documents()
    summary = build_analytics_summary(documents)

    return jsonify({
        "success": True,
        "summary": summary,
        "user": {
            "id": g.user_id,
            "email": g.user_email,
        },
    })
