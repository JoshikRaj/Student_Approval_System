from constants import UNALLOCATED, APPROVED, DECLINED, ONHOLD
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, Date,UniqueConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True)
    application_number = db.Column(String, nullable=False) 
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
    course_type = db.Column(String)  # e.g., 'self-finance' or 'aided'

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

class CourseStatus(db.Model):
    __tablename__ = 'course_statuses'
    
    id = db.Column(Integer, primary_key=True)
    course_name = db.Column(String, nullable=False)
    course_type = db.Column(String, nullable=False)  
    allocated_seats = db.Column(Integer, default=0)
    total_seats = db.Column(Integer, nullable=False)

    def __init__(self, course_name, course_type, total_seats, allocated_seats=0):
        self.course_name = course_name
        self.course_type = course_type
        self.total_seats = total_seats
        self.allocated_seats = allocated_seats

class TcartsStudent(db.Model):
    __tablename__ = 'tcarts_students'

    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)  
    gender = db.Column(db.String)
    school = db.Column(db.String)
    aadhar = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    alternate_number = db.Column(db.String)
    email = db.Column(db.String)
    community = db.Column(db.String)
    college = db.Column(db.String)
    degree = db.Column(db.String)
    degreeType = db.Column(db.String)
    course = db.Column(db.String)
    board = db.Column(db.String(100))
    year = db.Column(db.String)
    applicationstatus = db.Column(db.String)
    twelfth_mark = db.Column(db.Integer)
    date_of_application = db.Column(db.Date)
    subject1 = db.Column(db.Integer)
    subject2 = db.Column(db.Integer)
    subject3 = db.Column(db.Integer)
    subject4 = db.Column(db.Integer)
    cutoff = db.Column(db.Float)

    recommenders = db.relationship('TcartsRecommender', backref='student', cascade="all, delete-orphan")
    outcomes = db.relationship('TcartsAdmissionOutcome', backref='student', cascade="all, delete-orphan")

class TcartsRecommender(db.Model):
    __tablename__ = 'tcarts_recommenders'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('tcarts_students.id'), nullable=False)

    name = db.Column(db.String)
    designation = db.Column(db.String)
    affiliation = db.Column(db.String)
    office_address = db.Column(db.String)

    offcode = db.Column(db.String)
    percode = db.Column(db.String)

    office_phone_number = db.Column(db.String)
    personal_phone_number = db.Column(db.String)
    email = db.Column(db.String)

class TcartsAdmissionOutcome(db.Model):
    __tablename__ = 'tcarts_admission_outcomes'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('tcarts_students.id'), nullable=False)

    status = db.Column(db.String, default=UNALLOCATED)
    comments = db.Column(db.String)
    course_type = db.Column(db.String)  # e.g., 'self-finance' or 'aided'

    def __init__(self, student_id, status=UNALLOCATED, comments=None, course_type='self-finance'):
        self.student_id = student_id
        self.status = status
        self.comments = comments
        self.course_type = course_type

class TcartsCourseStatus(db.Model):
    __tablename__ = 'tcarts_course_statuses'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String, nullable=False)
    course_type = db.Column(db.String, nullable=False)  # e.g., 'Aided', 'Self Finance'
    allocated_seats = db.Column(db.Integer, default=0)
    total_seats = db.Column(db.Integer, nullable=False)

    def __init__(self, course_name, course_type, total_seats, allocated_seats=0):
        self.course_name = course_name
        self.course_type = course_type
        self.total_seats = total_seats
        self.allocated_seats = allocated_seats
