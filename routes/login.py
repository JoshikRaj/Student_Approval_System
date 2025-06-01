from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash
from auth import generate_token
from models import User
  # Only needed if you store token in DB

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login():
    # Validate JSON input
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Find the user
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        token = generate_token(user.id,user.email)

        

        return jsonify({
            "message": "Your login is successful",
            "success": True,
            "is_admin": user.is_admin,
            "token": token
        }), 200
    else:
        return jsonify({
            "message": "Invalid credentials. Please enter a valid email or password",
            "success": False
        }), 401
