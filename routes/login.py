from flask import app, request, jsonify, Blueprint
from werkzeug.security import check_password_hash

from models import User
login_bp=Blueprint('login', __name__)
@login_bp.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        return jsonify({
            "message": "Login successful",
            "success": True,
            "is_admin": user.is_admin
        })
    else:
        return jsonify({
            "message": "Invalid credentials",
            "success": False
        })
