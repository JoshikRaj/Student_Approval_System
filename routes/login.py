from flask import request, jsonify,Blueprint
from werkzeug.security import check_password_hash
from models import User
login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    # Check if user exists and password matches
    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "Login successful", "success": True})
    else:
        return jsonify({"message": "Invalid credentials", "success": False})
