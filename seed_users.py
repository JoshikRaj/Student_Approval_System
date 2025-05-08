from models import db, User
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

admin_email = "abs@gmail.com"
admin_password = "abc123"

other_users = [
    {"email": "user1@example.com", "password": "pass1", "isadmin": "yes"},
    {"email": "user2@example.com", "password": "pass2", "isadmin": "no"},
    {"email": "user3@example.com", "password": "pass3", "isadmin": "no"}
]

with app.app_context():
    db.create_all()

    # Create or update admin
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(email=admin_email)
        db.session.add(admin_user)

    admin_user.is_admin = True
    admin_user.password_hash = generate_password_hash(admin_password)

    # Create or update other users
    for u in other_users:
        user = User.query.filter_by(email=u["email"]).first()
        is_admin = u["isadmin"].lower() == "yes"

        if not user:
            user = User(email=u["email"])
            db.session.add(user)

        user.is_admin = is_admin
        user.password_hash = generate_password_hash(u["password"])

    db.session.commit()
    print("Users created or updated successfully.")
