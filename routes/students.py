from flask import Blueprint, jsonify, request
from models import db, Student, Recommender, AdmissionOutcome
from sqlalchemy.exc import IntegrityError
from datetime import datetime

#student_bp = Blueprint('students', __name__)
student_bp = Blueprint('students', __name__, url_prefix='/api/students')

@student_bp.route('', methods=['POST'])
def add_student():
    data = request.get_json()
    print("Received student POST request:", data) 
    try:
        date_str = data.get('date_of_application')
        date_of_application = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()

        aadhar_number = data.get('aadhar_number')
        application_number = data.get('application_number')

        existing_student = Student.query.filter(
            (Student.aadhar_number == aadhar_number) | 
            (Student.application_number == application_number)
        ).first()

        recommender_data = data.get('recommender')
        recommender_name = recommender_data.get('name') if recommender_data else None

        if existing_student:
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
                    "student_id": existing_student.id,
                    "status": 200
                }), 200
            else:
                return jsonify({
                    "error": "Student already exists with same recommender or no recommender provided.",
                    "status": 400
                }), 400

        # Degree and conditional cutoff logic
        degree = (data.get('degree') or '').strip().lower()
        maths = data.get('maths')
        physics = data.get('physics')
        chemistry = data.get('chemistry')
        nata = data.get('nata')
        engineering_cutoff = data.get('engineering_cutoff')
        msc_cutoff = data.get('msc_cutoff')
        barch_cutoff = data.get('barch_cutoff')
        bdes_cutoff = data.get('bdes_cutoff')

        # Validate degree-specific fields
        if degree == 'msc':
            required = [maths, physics, chemistry, msc_cutoff]
            if any(v is None for v in required):
                return jsonify({
                    "error": "Missing fields for MSc (maths, physics, chemistry, msc_cutoff)",
                    "status": 400
                }), 400
            engineering_cutoff = nata = barch_cutoff = bdes_cutoff = None

        elif degree in ['be', 'btech', 'be/btech']:
            required = [maths, physics, chemistry, engineering_cutoff]
            if any(v is None for v in required):
                return jsonify({
                    "error": "Missing fields for BE/BTech (maths, physics, chemistry, engineering_cutoff)",
                    "status": 400
                }), 400
            msc_cutoff = nata = barch_cutoff = bdes_cutoff = None

        elif degree == 'barch':
            required = [nata, barch_cutoff]
            if any(v is None for v in required):
                return jsonify({
                    "error": "Missing fields for BArch (nata, barch_cutoff)",
                    "status": 400
                }), 400
            engineering_cutoff = msc_cutoff = bdes_cutoff = None

        elif degree == 'bdes':
            required = [maths, physics, chemistry, bdes_cutoff]
            if any(v is None for v in required):
                return jsonify({
                    "error": "Missing fields for BDes (maths, physics, chemistry, bdes_cutoff)",
                    "status": 400
                }), 400
            engineering_cutoff = nata = msc_cutoff = barch_cutoff = None

        else:
            return jsonify({
                "error": f"Invalid degree: '{degree}'. Must be one of ['msc', 'be', 'btech', 'barch', 'bdes']",
                "status": 400
            }), 400

        # Create new student
        student = Student(
            application_number=application_number,
            name=data.get('name'),
            school=data.get('school'),
            district=data.get('district'),
            address=data.get('address'),
            stdcode=data.get('stdcode'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            aadhar_number=aadhar_number,
            parent_annual_income=data.get('parent_annual_income'),
            community=data.get('community'),
            college=data.get('college'),
            degree=degree,
            branch_1=data.get('branch_1'),
            branch_2=data.get('branch_2'),
            branch_3=data.get('branch_3'),
            board=data.get('board'),
            maths=maths,
            physics=physics,
            chemistry=chemistry,
            nata=nata,
            msc_cutoff=msc_cutoff,
            barch_cutoff=barch_cutoff,
            bdes_cutoff=bdes_cutoff,
            applicationstatus=data.get('applicationstatus'),
            twelfth_mark=data.get('twelfth_mark'),
            markpercentage=data.get('markpercentage'),
            engineering_cutoff=engineering_cutoff,
            year_of_passing=data.get('year_of_passing'),
            date_of_application=date_of_application
        )
        db.session.add(student)
        db.session.flush()

        # Add recommender if provided
        if recommender_data:
            recommender = Recommender(
                student_id=student.id,
                name=recommender_name,
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

        # Add default admission outcome
        admission_outcome = AdmissionOutcome(student_id=student.id)
        db.session.add(admission_outcome)

        db.session.commit()

        return jsonify({
            "message": "New student and recommender added successfully.",
            "id": student.id,
            "status": 201
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Student with this Aadhar number or application number already exists.",
            "status": 400
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": 500
        }), 500
