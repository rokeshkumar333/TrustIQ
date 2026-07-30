import os
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
except ImportError:  # pragma: no cover - depends on local environment
    psycopg2 = None

connection = None


def connect():
    global connection

    if connection is not None:
        return connection

    if psycopg2 is None:
        print("⚠️ psycopg2 is not installed; database features will be unavailable.")
        return None

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            connect_timeout=2,
        )
        print("✅ Database Connected Successfully!")
    except Exception as exc:
        connection = None
        print(f"⚠️ Database unavailable: {exc}")

    return connection


def initialize_database():
    db = connect()
    if db is None:
        return

    with db.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                original_filename VARCHAR(255) NOT NULL,
                stored_filename VARCHAR(255) NOT NULL,
                file_path TEXT NOT NULL,
                file_type VARCHAR(50),
                extracted_text TEXT DEFAULT '',
                trust_score INTEGER DEFAULT 0,
                status VARCHAR(50) DEFAULT 'Not Processed',
                metadata JSONB DEFAULT '{}'::jsonb,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("ALTER TABLE documents ADD COLUMN IF NOT EXISTS trust_score INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE documents ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'Not Processed'")
        cursor.execute("ALTER TABLE documents ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb")

    db.commit()


initialize_database()