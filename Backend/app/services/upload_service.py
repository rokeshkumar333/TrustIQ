import os

from app.config.database import connection


def save_document_details(
    user_id,
    original_filename,
    stored_filename,
    file_path,
    file_type
):

    cursor = connection.cursor()

    query = """
    INSERT INTO documents
    (
        user_id,
        original_filename,
        stored_filename,
        file_path,
        file_type
    )
    VALUES
    (%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            user_id,
            original_filename,
            stored_filename,
            file_path,
            file_type
        )
    )

    connection.commit()

    cursor.close()