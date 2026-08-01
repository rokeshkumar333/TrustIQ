import os
import json

from app.config.database import connect


def serialize_document_row(row):
    if row is None:
        return None

    fields = {}
    qr_verification = {}
    if len(row) > 9 and row[9]:
        try:
            metadata = json.loads(row[9]) if isinstance(row[9], str) else row[9]
            if isinstance(metadata, dict):
                qr_verification = metadata.pop("qr_verification", {})
                fields = metadata
            else:
                fields = {}
        except (TypeError, ValueError):
            fields = {}
            qr_verification = {}

    return {
        "id": row[0],
        "original_filename": row[1],
        "stored_filename": row[2],
        "file_path": row[3],
        "file_type": row[4],
        "ocr_text": row[5],
        "uploaded_at": str(row[6]),
        "trust_score": row[7] if len(row) > 7 else 0,
        "status": row[8] if len(row) > 8 else "Not Processed",
        "fields": fields,
        "qr_verification": qr_verification,
    }


def get_all_documents():
    db = connect()
    if db is None:
        return []

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text,
            uploaded_at,
            trust_score,
            status,
            metadata
        FROM documents
        ORDER BY uploaded_at DESC
    """)

    data = cursor.fetchall()

    cursor.close()

    return [serialize_document_row(row) for row in data]


def get_document_by_id(document_id):
    db = connect()
    if db is None:
        return None

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text,
            uploaded_at,
            trust_score,
            status,
            metadata
        FROM documents
        WHERE id=%s
    """, (document_id,))

    data = cursor.fetchone()

    cursor.close()

    return serialize_document_row(data)


def delete_document(document_id):
    db = connect()
    if db is None:
        return False

    cursor = db.cursor()

    cursor.execute(
        "SELECT file_path FROM documents WHERE id=%s",
        (document_id,)
    )

    row = cursor.fetchone()

    if row is None:

        cursor.close()

        return False

    filepath = row[0]

    if os.path.exists(filepath):
        os.remove(filepath)

    cursor.execute(
        "DELETE FROM documents WHERE id=%s",
        (document_id,)
    )

    db.commit()

    cursor.close()

    return True