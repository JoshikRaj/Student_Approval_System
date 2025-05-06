from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Import your models
from models import Base, User, Student, YearOfPassing, Recommender, AdmissionOutcome

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create all tables
with app.app_context():
    Base.metadata.create_all(bind=db.engine)

@app.route('/')
def home():
    return "Student Approval System API is running!"

# Example: Add a new student
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    try:
        student = Student(
            name=data.get('name'),
            school=data.get('school'),
            district=data.get('district'),
            address=data.get('address'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            aadhar_number=data.get('aadhar_number'),
            parent_annual_income=data.get('parent_annual_income'),
            community=data.get('community'),
            branch_1=data.get('branch_1'),
            branch_2=data.get('branch_2'),
            branch_3=data.get('branch_3'),
            date_of_application=datetime.strptime(data.get('date_of_application'), '%Y-%m-%d')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student added successfully", "id": student.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A student with this Aadhar number already exists."}), 400

# Example: Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    students = db.session.query(Student).all()
    result = []
    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "school": s.school,
            "district": s.district,
            "email": s.email,
            "aadhar_number": s.aadhar_number,
            "community": s.community,
            "date_of_application": s.date_of_application.strftime('%Y-%m-%d')
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
