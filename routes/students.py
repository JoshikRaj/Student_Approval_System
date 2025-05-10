from flask import Blueprint, jsonify, request
from models import db, Student, Recommender, AdmissionOutcome
from sqlalchemy.exc import IntegrityError
from datetime import datetime

student_bp = Blueprint('students', __name__)

@student_bp.route('', methods=['POST'])
@student_bp.route('', methods=['POST'])
def add_student():
    data = request.get_json()

    try:
        # Parse date safely
        date_str = data.get('date_of_application')
        date_of_application = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()

        # Get values to check duplicates
        aadhar_number = data.get('aadhar_number')
        application_number = data.get('application_number')

        # Check if student already exists
        existing_student = Student.query.filter(
            (Student.aadhar_number == aadhar_number) | 
            (Student.application_number == application_number)
        ).first()

        recommender_data = data.get('recommender')
        recommender_name = recommender_data.get('name') if recommender_data else None

        if existing_student:
            # Check if the same recommender already exists
            existing_recommender = Recommender.query.filter_by(
                student_id=existing_student.id,
                name=recommender_name
            ).first()

            if not existing_recommender and recommender_data:
                new_recommender = Recommender(
                    student_id=existing_student.id,
                    name=recommender_name,
                    designation=recommender_data.get('designation'),
                    affiliation=recommender_data.get('affiliation'),
                    office_address=recommender_data.get('office_address'),
                    office_phone_number=recommender_data.get('office_phone_number'),
                    personal_phone_number=recommender_data.get('personal_phone_number'),
                    email=recommender_data.get('email')
                )
                db.session.add(new_recommender)
                db.session.commit()

                return jsonify({
                    "message": "Recommender added to existing student.",
                    "student_id": existing_student.id
                }), 200
            else:
                return jsonify({
                    "error": "Student already exists with same recommender or no recommender provided."
                }), 400

        # Else create a new student
        student = Student(
            application_number=application_number,
            name=data.get('name'),
            school=data.get('school'),
            district=data.get('district'),
            address=data.get('address'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            aadhar_number=aadhar_number,
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
        db.session.flush()  # Gets student.id

        # Add recommender if provided
        if recommender_data:
            recommender = Recommender(
                student_id=student.id,
                name=recommender_name,
                designation=recommender_data.get('designation'),
                affiliation=recommender_data.get('affiliation'),
                office_address=recommender_data.get('office_address'),
                office_phone_number=recommender_data.get('office_phone_number'),
                personal_phone_number=recommender_data.get('personal_phone_number'),
                email=recommender_data.get('email')
            )
            db.session.add(recommender)

        # Add default AdmissionOutcome
        admission_outcome = AdmissionOutcome(student_id=student.id)
        db.session.add(admission_outcome)

        db.session.commit()

        return jsonify({
            "message": "New student and recommender added successfully.",
            "id": student.id
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Student with this Aadhar number or application number already exists."
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Unexpected error: {str(e)}"
        }), 500

