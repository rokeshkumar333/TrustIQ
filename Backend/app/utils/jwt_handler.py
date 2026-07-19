import jwt
import datetime

# ==========================================================
# TEMPORARY SECRET KEY
# (Later we will read it from .env)
# ==========================================================

SECRET_KEY = "TrustIQ2026"

# ==========================================================
# Generate JWT Token
# ==========================================================

def generate_token(user_email):

    payload = {

        "email": user_email,

        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)

    }

    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm="HS256"

    )

    return token

# ==========================================================
# Verify JWT Token
# ==========================================================

def verify_token(token):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=["HS256"]

        )

        return payload

    except jwt.ExpiredSignatureError:

        return None

    except jwt.InvalidTokenError:

        return None