from flask import Blueprint, jsonify
from auth import token_required

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/api/protected', methods=['GET'])
@token_required
def protected_route(user_id, user_email):
    return jsonify(message=f"Access granted to user {user_id} ({user_email})!")
