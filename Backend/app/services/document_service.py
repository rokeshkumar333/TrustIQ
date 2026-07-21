from app.config.database import connection


def get_all_documents():

    cursor = connection.cursor()

    query = """
    SELECT
        id,
        original_filename,
        stored_filename,
        file_path,
        file_type,
        uploaded_at
    FROM documents
    ORDER BY uploaded_at DESC
    """

    cursor.execute(query)

    documents = cursor.fetchall()

    cursor.close()

    return documents