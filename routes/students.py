from flask import Blueprint, jsonify, request
from models import db, Student, Recommender, AdmissionOutcome
from sqlalchemy.exc import IntegrityError
from datetime import datetime

student_bp = Blueprint('students', __name__)

@student_bp.route('', methods=['POST'])
def add_student():
    data = request.json
    try:
        # Parse date separately before using in constructor
        date_str = data.get('date_of_application')
        date_of_application = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()

        # Step 1: Create Student
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
            college=data.get('college'),
            branch_1=data.get('branch_1'),
            branch_2=data.get('branch_2'),
            branch_3=data.get('branch_3'),
            board=data.get('board'),
            twelfth_mark=data.get('twelfth_mark'),
            markpercentage=data.get('markpercentage'),
            engineering_cutoff=data.get('engineering_cutoff'),
            year_of_passing=data.get('year_of_passing'),
            date_of_application=date_of_application
        )
        db.session.add(student)
        db.session.commit()

        # Step 2: Create Recommender (if exists)
        recommender_data = data.get('recommender')
        if recommender_data:
            recommender = Recommender(
                student_id=student.id,
                name=recommender_data.get('name'),
                designation=recommender_data.get('designation'),
                affiliation=recommender_data.get('affiliation'),
                office_address=recommender_data.get('office_address'),
                office_phone_number=recommender_data.get('office_phone_number'),
                personal_phone_number=recommender_data.get('personal_phone_number'),
                email=recommender_data.get('email')
            )
            db.session.add(recommender)
        admission_outcome = AdmissionOutcome(student_id=student.id)
        db.session.add(admission_outcome)

        db.session.commit()

        return jsonify({"message": "Student and Recommender added successfully", "id": student.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A student with this Aadhar number already exists."}), 400
