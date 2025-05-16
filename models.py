from constants import UNALLOCATED, APPROVED, DECLINED, ONHOLD
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, Date
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True)
    application_number = db.Column(String, unique=True, nullable=False) 
    name = db.Column(String)
    school = db.Column(String)
    district = db.Column(String)
    address = db.Column(String)
    stdcode = db.Column(String)
    phone_number = db.Column(String)
    email = db.Column(String)
    aadhar_number = db.Column(String)
    parent_annual_income = db.Column(DECIMAL)
    community = db.Column(String)
    college = db.Column(String)
    degree = db.Column(String)
    branch_1 = db.Column(String)
    branch_2 = db.Column(String)
    branch_3 = db.Column(String)
    board = db.Column(db.String(100)) 
    maths = db.Column(db.Float)
    physics = db.Column(db.Float)
    chemistry = db.Column(db.Float)
    nata = db.Column(db.Float)
    studybreak = db.Column(db.Integer)
    msc_cutoff = db.Column(db.Float)
    barch_cutoff = db.Column(db.Float)
    bdes_cutoff = db.Column(db.Float)
    twelfth_mark = db.Column(db.Integer) 
    markpercentage=db.Column(db.Float)
    engineering_cutoff = db.Column(db.Float)
    date_of_application = db.Column(Date)
    applicationstatus=db.Column(db.String) 
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
    offcode=db.Column(String)
    percode=db.Column(String)
    office_phone_number = db.Column(String)
    personal_phone_number = db.Column(String)
    email = db.Column(String)




class AdmissionOutcome(db.Model):
    __tablename__ = 'admission_outcomes'
    
    id = db.Column(Integer, primary_key=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    status = db.Column(String, default=UNALLOCATED)  # Default status
    comments = db.Column(String)
    
    # New column for course type
    course_type = db.Column(String, nullable=False)  # e.g., 'self-finance' or 'aided'

    def __init__(self, student_id, status=UNALLOCATED, comments=None, course_type='self-finance'):
        self.student_id = student_id
        self.status = status
        self.comments = comments
        self.course_type = course_type


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String, unique=True, nullable=False)
    password_hash = db.Column(String, nullable=False)
    is_admin = db.Column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    