from models import db, User
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Update path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

admin_email = "abs@gmail.com"
admin_password = "abc123"

other_users = [
    {"email": "user1@example.com", "password": "pass1"},
    {"email": "user2@example.com", "password": "pass2"},
    {"email": "user3@example.com", "password": "pass3"}
]

with app.app_context():
    db.create_all()

    # Create admin
    if not User.query.filter_by(email=admin_email).first():
        admin_user = User(email=admin_email, is_admin=True)
        admin_user.password_hash = generate_password_hash(admin_password)
        db.session.add(admin_user)

    # Create regular users
    for u in other_users:
        if not User.query.filter_by(email=u["email"]).first():
            user = User(email=u["email"], is_admin=False)
            user.password_hash = generate_password_hash(u["password"])
            db.session.add(user)

    db.session.commit()
    print("Users seeded successfully.")
