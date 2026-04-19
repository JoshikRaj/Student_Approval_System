import datetime
from flask import Blueprint, request, jsonify
from auth import generate_access_token
from models import db, RefreshToken

refresh_bp = Blueprint('refresh', __name__)

@refresh_bp.route('/api/refresh', methods=['POST'])
def refresh():
    """
    Exchange a valid refresh token for a new access token.
    Body: { "refresh_token": "<token>" }
    """
    data = request.get_json(silent=True) or {}
    token_str = data.get('refresh_token')

    if not token_str:
        return jsonify({"message": "Refresh token is missing!"}), 401

    # Check if the refresh token exists in DB and is not revoked
    stored = RefreshToken.query.filter_by(token=token_str, is_revoked=False).first()
    if not stored:
        return jsonify({"message": "Refresh token is invalid or has been revoked!"}), 401

    if stored.expires_at < datetime.datetime.utcnow():
        stored.is_revoked = True
        db.session.commit()
        return jsonify({"message": "Refresh token has expired! Please log in again."}), 401

    # Issue new access token
    new_access_token = generate_access_token(stored.user_id, stored.user_email)
    return jsonify({"access_token": new_access_token}), 200
