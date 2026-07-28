from flask import Blueprint, request, jsonify
from app.config.database import connection
from app.utils.jwt_handler import generate_token
from app.utils.auth_middleware import token_required
import bcrypt

auth = Blueprint("auth", __name__)


# ==========================================================
# REGISTER
# ==========================================================
@auth.route("/register", methods=["POST"])
def register():

    cursor = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No JSON data received."
            }), 400

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")

        if not full_name or not email or not password:

            return jsonify({
                "success": False,
                "message": "All fields are required."
            }), 400

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return jsonify({
                "success": False,
                "message": "Email already exists."
            }), 400

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                full_name,
                email,
                hashed_password
            )
        )

        connection.commit()

        return jsonify({

            "success": True,
            "message": "User Registered Successfully"

        }), 201

    except Exception as e:

        if connection:
            connection.rollback()

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

    finally:

        if cursor:
            cursor.close()
# ==========================================================
# LOGIN
# ==========================================================
@auth.route("/login", methods=["POST"])
def login():

    cursor = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No JSON data received."
            }), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:

            return jsonify({
                "success": False,
                "message": "Email and Password are required."
            }), 400

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                full_name,
                email,
                password
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "success": False,
                "message": "Email not found."
            }), 404

        user_id = user[0]
        full_name = user[1]
        user_email = user[2]
        hashed_password = user[3]

        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

        if not password_match:

            return jsonify({
                "success": False,
                "message": "Incorrect Password."
            }), 401

        token = generate_token(
            user_id=user_id,
            user_email=user_email
        )

        return jsonify({

            "success": True,
            "message": "Login Successful",
            "token": token,

            "user": {

                "id": user_id,
                "full_name": full_name,
                "email": user_email

            }

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

    finally:

        if cursor:
            cursor.close()


# ==========================================================
# PROFILE
# ==========================================================
@auth.route("/profile", methods=["GET"])
@token_required
def profile():

    return jsonify({

        "success": True,
        "message": "Welcome to TrustIQ Secure API"

    })