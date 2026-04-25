import datetime
from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash
from auth import generate_access_token, generate_refresh_token
from models import User, db, RefreshToken
from flask_cors import cross_origin

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
@cross_origin()
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
        access_token = generate_access_token(user.id, user.email)
        refresh_token = generate_refresh_token(user.id, user.email)

        # Persist the refresh token in DB
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        rt = RefreshToken(
            user_id=user.id,
            user_email=user.email,
            token=refresh_token,
            expires_at=expires_at
        )
        db.session.add(rt)
        db.session.commit()

        return jsonify({
            "message": "Your login is successful",
            "success": True,
            "is_admin": user.is_admin,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    else:
        return jsonify({
            "message": "Invalid credentials. Please enter a valid email or password",
            "success": False
        }), 401
