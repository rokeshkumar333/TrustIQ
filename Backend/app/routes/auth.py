from flask import Blueprint, request, jsonify
from app.config.database import connection
from app.utils.jwt_handler import generate_token
import bcrypt

auth = Blueprint("auth", __name__)


# ===============================
# REGISTER API
# ===============================
@auth.route("/register", methods=["POST"])
def register():

    cursor = None

    try:

        data = request.get_json()

        full_name = data["full_name"]
        email = data["email"]
        password = data["password"]

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor = connection.cursor()

        # Check Duplicate Email
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return jsonify({
                "success": False,
                "message": "Email already registered."
            }), 400

        cursor.execute(
            """
            INSERT INTO users(full_name,email,password)
            VALUES(%s,%s,%s)
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

        connection.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()


# ===============================
# LOGIN API
# ===============================
@auth.route("/login", methods=["POST"])
def login():

    cursor = None

    try:

        data = request.get_json()

        email = data["email"]
        password = data["password"]

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id,full_name,email,password
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "success": False,
                "message": "Email not found"
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
                "message": "Incorrect Password"
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

        connection.rollback()

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

    finally:

        if cursor:
            cursor.close()
    
from app.utils.auth_middleware import token_required


@auth.route("/profile", methods=["GET"])
@token_required
def profile():

    return jsonify({

        "success": True,
        "message": "Welcome to TrustIQ Secure API"

    })