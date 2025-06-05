# import jwt
# import datetime
# from functools import wraps
# from flask import request, jsonify
# import os
# # Generate a JWT token with a 1-hour expiration
# def generate_token(user_id,user_email):
#     payload = {
#         'user_id': user_id,
#         'user_email':user_email,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
#     }
#     token = jwt.encode(payload, os.getenv['SECRET_KEY'], algorithm='HS256')
#     return token


# # Decorator to protect routes using JWT token
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         # Expecting header: Authorization: Bearer <token>
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             parts = auth_header.split()
#             if len(parts) == 2 and parts[0].lower() == 'bearer':
#                 token = parts[1]

#         if not token:
#             return jsonify({"message": "Token is missing!"}), 401

#         try:
#             payload = jwt.decode(token, os.getenv['SECRET_KEY'], algorithms=['HS256'])
#             user_id = payload['user_id']
#             user_email=payload['user_email']
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token has expired!"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token!"}), 401

#         return f(user_id, user_email,*args, **kwargs)

#     return decorated
