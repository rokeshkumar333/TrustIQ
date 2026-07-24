from flask import Blueprint, jsonify

from app.services.document_service import (
    get_all_documents,
    get_document_by_id,
    delete_document
)

documents = Blueprint("documents", __name__)


@documents.route("/documents", methods=["GET"])
def document_history():

    rows = get_all_documents()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "original_filename": row[1],
            "stored_filename": row[2],
            "file_path": row[3],
            "file_type": row[4],
            "ocr_text": row[5],
            "uploaded_at": str(row[6])
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "documents": result
    })


@documents.route("/documents/<int:document_id>", methods=["GET"])
def document_details(document_id):

    row = get_document_by_id(document_id)

    if row is None:

        return jsonify({
            "success": False,
            "message": "Document not found"
        }), 404

    return jsonify({

        "success": True,

        "document": {

            "id": row[0],
            "original_filename": row[1],
            "stored_filename": row[2],
            "file_path": row[3],
            "file_type": row[4],
            "ocr_text": row[5],
            "uploaded_at": str(row[6])

        }

    })


@documents.route("/documents/<int:document_id>", methods=["DELETE"])
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