from flask import Blueprint, jsonify, request
from models import db, Student, Recommender, AdmissionOutcome
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from auth import token_required

#student_bp = Blueprint('students', __name__)
student_bp = Blueprint('students', __name__, url_prefix='/api/students')

@student_bp.route('', methods=['POST'])
@token_required
def add_student(user_id, user_email):
    data = request.get_json()
    print("Received student POST request:", data) 

    try:
        date_str = data.get('date_of_application')
        date_of_application = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()

        aadhar_number = data.get('aadhar_number')
        application_number = data.get('application_number')

        # Removed the existing_student duplicate check

        # Program type and degree validation
        program_type = (data.get('program_type') or '').strip().lower()
        degree = (data.get('degree') or '').strip().lower()
        print(f"DEBUG-INPUT program_type={program_type!r} degree={degree!r}")

        # Auto-fallback program_type from degree when missing
        pg_degrees = ['me_mtech', 'march', 'mca']
        ug_degrees = ['btech', 'be', 'msc', 'bdes', 'barch']

        if not program_type:
            if degree in pg_degrees:
                program_type = 'pg'
            elif degree in ug_degrees:
                program_type = 'ug'

        maths = data.get('maths')
        physics = data.get('physics')
        chemistry = data.get('chemistry')
        nata = data.get('nata')
        engineering_cutoff = data.get('engineering_cutoff')
        msc_cutoff = data.get('msc_cutoff')
        barch_cutoff = data.get('barch_cutoff')
        bdes_cutoff = data.get('bdes_cutoff')
        is_confirm = data.get('is_confirm')

        # PG-specific required data
        ug_consolidated_mark = data.get('ug_consolidated_mark')
        ug_course_name = data.get('ug_course_name')
        ug_institution = data.get('ug_institution')
        tancet_gate_score = data.get('tancet_gate_score')

        if program_type not in ['ug', 'pg', 'lateral']:
            return jsonify({
                "error": "Invalid program_type: must be one of 'UG', 'PG', 'Lateral'",
                "status": 400
            }), 400

        if program_type == 'pg':
            if ug_consolidated_mark is None or ug_course_name is None or ug_institution is None:
                return jsonify({
                    "error": "Missing PG required fields: ug_consolidated_mark, ug_course_name, ug_institution",
                    "status": 400
                }), 400

        # Validate degree-specific fields (only when not PG)
        if program_type != 'pg':
            if degree == 'msc':
                if not msc_cutoff:
                    return jsonify({
                        "error": "Missing fields for MSc (msc_cutoff)",
                        "status": 400
                    }), 400
                engineering_cutoff = nata = barch_cutoff = bdes_cutoff = None

            elif degree in ['be', 'btech', 'be/btech']:
                if not engineering_cutoff:
                    return jsonify({
                        "error": "Missing fields for BE/BTech (engineering_cutoff)",
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
                if not bdes_cutoff:
                    return jsonify({
                        "error": "Missing fields for BDes (bdes_cutoff)",
                        "status": 400
                    }), 400
                engineering_cutoff = nata = msc_cutoff = barch_cutoff = None

            else:
                return jsonify({
                    # "error": f"Invalid degree: '{degree}'. Must be one of ['msc', 'be', 'btech', 'barch', 'bdes', 'me_mtech', 'march', 'mca']",

                    "error": f"INVALID-DEGREE-DEBUG: '{degree}' => Must include me_mtech/march/mca (PG possible)",
                    "status": 400
                }), 400
        else:
            # PG mode: do not enforce cutoff checks, reset these fields
            engineering_cutoff = msc_cutoff = barch_cutoff = bdes_cutoff = nata = None
        print("abjhd")
        other_record = Student.query.filter(
            Student.application_number == application_number,
        ).first()
        print(other_record)
        if(other_record and not is_confirm):
            return jsonify({
                "error": f"Record Duplicate:. There is an existing record for this application number",
                "status": 409
            }), 409

        # Insert student
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
            program_type=program_type,
            ug_consolidated_mark=ug_consolidated_mark,
            ug_course_name=ug_course_name,
            ug_institution=ug_institution,
            tancet_gate_score=tancet_gate_score,
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
        db.session.flush()  # Ensure student.id is available

        # Add recommender
        recommender_data = data.get('recommender')
        if recommender_data:
            recommender = Recommender(
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

        # Add admission outcome
        admission_outcome = AdmissionOutcome(student_id=student.id, status='UNALLOCATED')
        db.session.add(admission_outcome)

        db.session.commit()

        return jsonify({
            "message": "Student and recommender inserted successfully.",
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
        
        
        
        