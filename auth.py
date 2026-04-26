import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY', 'dev-refresh-secret-key')

# ─── Token Generators ────────────────────────────────────────────────────────

def generate_access_token(user_id, user_email):
    """Short-lived access token: expires in 15 minutes."""
    payload = {
        'user_id': user_id,
        'user_email': user_email,
        'type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user_id, user_email):
    """Long-lived refresh token: expires in 7 days."""
    payload = {
        'user_id': user_id,
        'user_email': user_email,
        'type': 'refresh',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')


# ─── Decorators ───────────────────────────────────────────────────────────────

def token_required(f):
    """Protect a route — expects Authorization: Bearer <access_token>."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Always let CORS preflight requests through — never block OPTIONS
        if request.method == 'OPTIONS':
            return '', 204

        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            return jsonify({"message": "Access token is missing!"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'access':
                return jsonify({"message": "Invalid token type!"}), 401
            user_id = payload['user_id']
            user_email = payload['user_email']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Access token has expired!", "expired": True}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid access token!"}), 401

        return f(user_id, user_email, *args, **kwargs)

    return decorated


def refresh_token_required(f):
    """Validate a refresh token — used only on the /api/refresh endpoint."""
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json(silent=True) or {}
        token = data.get('refresh_token')

        if not token:
            return jsonify({"message": "Refresh token is missing!"}), 401

        try:
            payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'refresh':
                return jsonify({"message": "Invalid token type!"}), 401
            user_id = payload['user_id']
            user_email = payload['user_email']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Refresh token has expired! Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid refresh token!"}), 401

        return f(user_id, user_email, token, *args, **kwargs)

    return decorated
