import json

from app.config.database import connect


def save_document_details(
    user_id,
    original_filename,
    stored_filename,
    file_path,
    file_type,
    extracted_text="",
    trust_score=0,
    status="Not Processed",
    fields=None,
    qr_verification=None,
):
    db = connect()
    if db is None:
        return

    cursor = db.cursor()

    metadata = json.dumps({
        **(fields or {}),
        "qr_verification": qr_verification or {},
    }, default=str)

    cursor.execute(
        """
        INSERT INTO documents
        (
            user_id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text,
            trust_score,
            status,
            metadata
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            user_id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text,
            trust_score,
            status,
            metadata,
        )
    )

    db.commit()

    cursor.close()