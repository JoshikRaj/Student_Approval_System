from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recommender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    office_name = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    decision = db.Column(db.String(50))  # Accepted, On Hold, Declined

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    capacity = db.Column(db.Integer, default=180)
    filled = db.Column(db.Integer, default=0)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    school = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address = db.Column(db.Text)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    marks = db.Column(db.Text)  # JSON string (you can parse in frontend/backend)
    cutoff = db.Column(db.Float)
    aadhar = db.Column(db.String(12))
    income = db.Column(db.Integer)
    branches = db.Column(db.Text)  # Store as comma-separated
    date_applied = db.Column(db.String(20))
    recommender_id = db.Column(db.Integer, db.ForeignKey('recommender.id'))

class StudentStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    recommender_id = db.Column(db.Integer, db.ForeignKey('recommender.id'))
