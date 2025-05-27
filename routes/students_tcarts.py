from flask import Blueprint, jsonify, request
from models import db, TcartsStudent, TcartsRecommender, TcartsAdmissionOutcome
from sqlalchemy.exc import IntegrityError
from datetime import datetime

tcarts_student_bp = Blueprint('tcarts_student', __name__, url_prefix='/api/tcarts/students')

@tcarts_student_bp.route('', methods=['POST'])
def add_tcarts_student():
    data = request.get_json()
    print("Received tcarts student POST request:", data)

    try:
        # Parse date fields safely
        date_of_application_str = data.get('date_of_application')
        date_of_application = datetime.strptime(date_of_application_str, '%Y-%m-%d').date() if date_of_application_str else None

        dob_str = data.get('date_of_birth')
        date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None

        student = TcartsStudent(
            application_number=data.get('application_number'),
            name=data.get('name'),
            gender=data.get('gender'),
            date_of_birth=date_of_birth,
            school=data.get('school'),
            address=data.get('address'),
            phone_number=data.get('phone_number'),
            alternate_number=data.get('alternate_number'),
            email=data.get('email'),
            community=data.get('community'),
            college=data.get('college'),
            board=data.get('board'),
            degreeType=data.get('degreeType'),
            degree=data.get('degree'),
            course=data.get('course'),
            year=data.get('year'),
            applicationstatus=data.get('applicationstatus'),
            subject1=data.get('subject1'),
            subject2=data.get('subject2'),
            subject3=data.get('subject3'),
            subject4=data.get('subject4'),
            aadhar=data.get('aadhar_number'),
            cutoff=data.get('cutoff'),
            twelfth_mark=data.get('twelfth_mark'),
            date_of_application=date_of_application
        )
        db.session.add(student)
        db.session.flush()  # To get student.id

        # Add recommender if provided
        recommender_data = data.get('recommender')
        if recommender_data:
            recommender = TcartsRecommender(
                student_id=student.id,
                name=recommender_data.get('name'),
                designation=recommender_data.get('designation'),
                affiliation=recommender_data.get('affiliation'),
                office_address=recommender_data.get('office_address'),
                offcode=recommender_data.get('offcode'),
                office_phone_number=recommender_data.get('office_phone_number'),
                percode=recommender_data.get('percode'),
                personal_phone_number=recommender_data.get('personal_phone_number'),
                email=recommender_data.get('email')
            )
            db.session.add(recommender)

        # Add admission outcome default status
        admission_outcome = TcartsAdmissionOutcome(student_id=student.id, status='UNALLOCATED')
        db.session.add(admission_outcome)

        db.session.commit()

        return jsonify({
            "message": "TCARTS student and recommender inserted successfully.",
            "id": student.id,
            "status": 201
        }), 201

    except IntegrityError as ie:
        db.session.rollback()
        return jsonify({
            "error": "Application Number already exists. Can't enter an existing application number.",
            "details": str(ie),
            "status": 400
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": 500
        }), 500
