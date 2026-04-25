from flask import Blueprint, request, jsonify
from auth import token_required
from models import db, RefreshToken

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/api/logout', methods=['POST'])
@token_required
def logout(user_id, user_email):
    """
    Revoke the refresh token so it can no longer be used.
    Body: { "refresh_token": "<token>" }
    """
    data = request.get_json(silent=True) or {}
    token_str = data.get('refresh_token')

    if token_str:
        stored = RefreshToken.query.filter_by(token=token_str, user_id=user_id).first()
        if stored:
            stored.is_revoked = True
            db.session.commit()

    return jsonify({"message": "Logged out successfully."}), 200
