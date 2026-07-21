from flask import Blueprint, jsonify

from app.services.document_service import get_all_documents

documents = Blueprint("documents", __name__)


@documents.route("/documents", methods=["GET"])
def document_history():

    data = get_all_documents()

    result = []

    for row in data:

        result.append({
            "id": row[0],
            "original_filename": row[1],
            "stored_filename": row[2],
            "file_path": row[3],
            "file_type": row[4],
            "uploaded_at": str(row[5])
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "documents": result
    })