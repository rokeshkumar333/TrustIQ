from flask import Blueprint, jsonify
from app.services.document_service import (
    get_all_documents,
    get_document_by_id,
    delete_document
)
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