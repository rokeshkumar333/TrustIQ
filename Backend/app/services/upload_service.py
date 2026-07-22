from app.config.database import connection


def save_document_details(
    user_id,
    original_filename,
    stored_filename,
    file_path,
    file_type,
    extracted_text=""
):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents
        (
            user_id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            user_id,
            original_filename,
            stored_filename,
            file_path,
            file_type,
            extracted_text
        )
    )

    connection.commit()

    cursor.close()