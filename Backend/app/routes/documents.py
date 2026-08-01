from flask import Blueprint, jsonify
from app.services.document_service import (
    get_all_documents,
    get_document_by_id,
    delete_document
)
from app.services.report_service import build_verification_report
from app.services.trust_score_service import calculate_ai_trust_score
from app.services.fraud_detection_service import analyze_fraud
from app.services.image_forgery_service import analyze_image_forgery
from app.services.signature_verification_service import inspect_pdf_signature
from app.utils.auth_middleware import token_required

documents = Blueprint("documents", __name__)


@documents.route("/documents", methods=["GET"])
@token_required
def document_history():
    rows = get_all_documents()

    return jsonify({
        "success": True,
        "count": len(rows),
        "documents": rows
    })


@documents.route("/documents/<int:document_id>", methods=["GET"])
@token_required
def document_details(document_id):
    row = get_document_by_id(document_id)

    if row is None:
        return jsonify({
            "success": False,
            "message": "Document not found"
        }), 404

    return jsonify({
        "success": True,
        "document": row
    })


@documents.route("/reports/<int:report_id>", methods=["GET"])
@token_required
def report_details(report_id):
    try:
        row = get_document_by_id(report_id)
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": "Unable to retrieve report",
            "error": str(exc)
        }), 500

    if row is None:
        return jsonify({
            "success": False,
            "message": "Report not found"
        }), 404

    report = build_verification_report(row, file_path=row.get("file_path"))
    image_forgery_analysis = analyze_image_forgery(row.get("file_path"))
    report["image_forgery_analysis"] = image_forgery_analysis
    trust_score = calculate_ai_trust_score(report)
    fraud_analysis = analyze_fraud({
        **row,
        "verification_report": report,
        "image_forgery_analysis": image_forgery_analysis,
    }, file_path=row.get("file_path"))
    signature_analysis = inspect_pdf_signature(row.get("file_path"))

    return jsonify({
        "success": True,
        "report": {
            **row,
            "verification_report": report,
            "image_forgery_analysis": image_forgery_analysis,
            "trust_score_engine": trust_score,
            "fraud_detection_engine": fraud_analysis,
            "signature_verification": signature_analysis,
            "report_summary": {
                "score": trust_score["overall_score"],
                "status": report["final_decision"],
                "risk_level": trust_score["risk_level"],
            },
        }
    })


@documents.route("/documents/<int:document_id>", methods=["DELETE"])
@token_required
def remove_document(document_id):
    deleted = delete_document(document_id)

    if deleted:
        return jsonify({
            "success": True,
            "message": "Document deleted successfully"
        })

    return jsonify({
        "success": False,
        "message": "Document not found"
    }), 404