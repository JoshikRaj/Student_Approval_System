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
            date_of_birth=date_of_birth,
            school=data.get('school'),
            district=data.get('district'),
            address=data.get('address'),
            stdcode=data.get('stdcode'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            parent_annual_income=data.get('parent_annual_income'),
            community=data.get('community'),
            college=data.get('college'),
            degree=data.get('degree'),
            board=data.get('board'),
            year_of_passing=data.get('year_of_passing'),
            applicationstatus=data.get('applicationstatus'),
            studybreak=data.get('studybreak'),
            tamil=data.get('tamil'),
            english=data.get('english'),
            maths=data.get('maths'),
            physics=data.get('physics'),
            chemistry=data.get('chemistry'),
            biology=data.get('biology'),
            computer_science=data.get('computer_science'),
            commerce=data.get('commerce'),
            accountancy=data.get('accountancy'),
            economics=data.get('economics'),
            business_math=data.get('business_math'),
            twelfth_mark=data.get('twelfth_mark'),
            markpercentage=data.get('markpercentage'),
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
