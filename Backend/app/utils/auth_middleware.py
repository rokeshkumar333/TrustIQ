from functools import wraps
from flask import request, jsonify, g

from app.utils.jwt_handler import verify_token


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Token is missing"
            }), 401

        try:
            token = auth_header.split(" ")[1]

        except IndexError:
            return jsonify({
                "success": False,
                "message": "Invalid Token Format"
            }), 401

        payload = verify_token(token)

        if payload is None:
            return jsonify({
                "success": False,
                "message": "Invalid or Expired Token"
            }), 401

        # Store logged-in user information
        g.user_id = payload["id"]
        g.user_email = payload["email"]

        return f(*args, **kwargs)

    return decorated