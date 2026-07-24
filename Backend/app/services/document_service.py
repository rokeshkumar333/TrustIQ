import os

from app.config.database import connection


def get_all_documents():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text,
            uploaded_at
        FROM documents
        ORDER BY uploaded_at DESC
    """)

    data = cursor.fetchall()

    cursor.close()

    return data


def get_document_by_id(document_id):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text,
            uploaded_at
        FROM documents
        WHERE id=%s
    """, (document_id,))

    data = cursor.fetchone()

    cursor.close()

    return data


def delete_document(document_id):

    cursor = connection.cursor()

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

    connection.commit()

    cursor.close()

    return True