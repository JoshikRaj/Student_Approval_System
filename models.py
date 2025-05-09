from constants import UNALLOCATED, APPROVED, DECLINED, ONHOLD
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, Date
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True)
    application_number = db.Column(String, unique=True) 
    name = db.Column(String)
    school = db.Column(String)
    district = db.Column(String)
    address = db.Column(String)
    phone_number = db.Column(String)
    email = db.Column(String)
    aadhar_number = db.Column(String, unique=True)
    parent_annual_income = db.Column(DECIMAL)
    community = db.Column(String)
    college=db.Column(String)
    branch_1 = db.Column(String)
    branch_2 = db.Column(String)
    branch_3 = db.Column(String)
    board = db.Column(db.String(100))  
    twelfth_mark = db.Column(db.Integer) 
    markpercentage=db.Column(db.Float)
    engineering_cutoff = db.Column(db.Float)
    date_of_application = db.Column(Date)
    year_of_passing = db.Column(String)
    recommenders = relationship('Recommender', backref='student', cascade="all, delete-orphan")
    outcomes = relationship('AdmissionOutcome', backref='student', cascade="all, delete-orphan")


class Recommender(db.Model):
    __tablename__ = 'recommenders'
    id = db.Column(Integer, primary_key=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    name = db.Column(String)
    designation = db.Column(String)
    affiliation = db.Column(String)
    office_address = db.Column(String)
    office_phone_number = db.Column(String)
    personal_phone_number = db.Column(String)
    email = db.Column(String)


class AdmissionOutcome(db.Model):
    __tablename__ = 'admission_outcomes'
    id = db.Column(Integer, primary_key=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    status = db.Column(String, default=UNALLOCATED)  # Default status
    comments = db.Column(String)

    def __init__(self, student_id, status=UNALLOCATED, comments=None):
        self.student_id = student_id
        self.status = status
        self.comments = comments

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String, unique=True, nullable=False)
    password_hash = db.Column(String, nullable=False)
    is_admin = db.Column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    