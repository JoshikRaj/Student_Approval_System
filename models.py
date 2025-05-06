from sqlalchemy import (
    Column, Integer, String, Boolean, Text, Date, DECIMAL, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    school = Column(String)
    district = Column(String)
    address = Column(Text)
    phone_number = Column(String)
    email = Column(String)
    aadhar_number = Column(String, unique=True)
    parent_annual_income = Column(DECIMAL)
    community = Column(String)
    branch_1 = Column(String)
    branch_2 = Column(String)
    branch_3 = Column(String)
    date_of_application = Column(Date)

class YearOfPassing(Base):
    __tablename__ = 'year_of_passing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    medium = Column(String)
    mark_mathematics = Column(Integer)
    mark_physics = Column(Integer)
    mark_chemistry = Column(Integer)
    engg_cutoff = Column(DECIMAL)
    break_of_study = Column(Boolean)

class Recommender(Base):
    __tablename__ = 'recommenders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    name = Column(String)
    designation = Column(String)
    affiliation = Column(String)
    office_address = Column(Text)
    office_phone = Column(String)
    personal_phone = Column(String)
    email = Column(String)

class AdmissionOutcome(Base):
    __tablename__ = 'admission_outcomes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    degree = Column(String)
    department = Column(String)  # Recommended department
    status = Column(String)
    branch_allotted = Column(String)  # Final branch allotted if status is Allotted
