from flask import Blueprint, jsonify, request
from models import TcartsStudent, TcartsAdmissionOutcome, TcartsRecommender
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

tcarts_students_bp = Blueprint('tcarts_students', __name__, url_prefix='/api/tcarts')

@tcarts_students_bp.route('/students', methods=['GET'])
def get_tcarts_students():
    print("Route /tcarts/students accessed")

    status_filter = request.args.get('status')
    college_filter = request.args.get('college')
    search_query = request.args.get('search')

    query = TcartsStudent.query.options(
        joinedload(TcartsStudent.recommenders),
        joinedload(TcartsStudent.outcomes)
    )

    if status_filter:
        query = query.join(TcartsAdmissionOutcome).filter(TcartsAdmissionOutcome.status == status_filter)

    if college_filter:
        query = query.filter(TcartsStudent.college == college_filter)

    if search_query:
        like_pattern = f"%{search_query}%"
        query = query.outerjoin(TcartsRecommender).filter(or_(
            TcartsStudent.name.ilike(like_pattern),
            TcartsStudent.application_number.ilike(like_pattern),
            TcartsRecommender.name.ilike(like_pattern),
            TcartsRecommender.affiliation.ilike(like_pattern),
            TcartsRecommender.designation.ilike(like_pattern)
        ))

    students = query.all()

    student_data = []
    for student in students:
        student_dict = {
            'id': student.id,
            'application_number': student.application_number,
            'name': student.name,
            'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else None,
            'school': student.school,
            'district': student.district,
            'email': student.email,
            'stdcode': student.stdcode,
            'parent_annual_income': student.parent_annual_income,
            'phone_number': student.phone_number,
            'community': student.community,
            'college': student.college,
            'degree': student.degree,
            'branch_1': student.branch_1,
            'branch_2': student.branch_2,
            'branch_3': student.branch_3,
            'board': student.board,
            'studybreak': student.studybreak,
            'twelfth_mark': student.twelfth_mark,
            'markpercentage': student.markpercentage,
            'applicationstatus': student.applicationstatus,
            'date_of_application': student.date_of_application.strftime('%Y-%m-%d') if student.date_of_application else None,
            'year_of_passing': student.year_of_passing,
            # 12th subject marks
            'tamil': student.tamil,
            'english': student.english,
            'maths': student.maths,
            'physics': student.physics,
            'chemistry': student.chemistry,
            'biology': student.biology,
            'computer_science': student.computer_science,
            'commerce': student.commerce,
            'accountancy': student.accountancy,
            'economics': student.economics,
            'business_math': student.business_math,

            'recommenders': [
                {
                    'name': rec.name,
                    'designation': rec.designation,
                    'affiliation': rec.affiliation,
                    'office_address': rec.office_address,
                    'offcode': rec.offcode,
                    'office_phone_number': rec.office_phone_number,
                    'percode': rec.percode,
                    'personal_phone_number': rec.personal_phone_number,
                    'email': rec.email
                } for rec in student.recommenders
            ],
            'outcomes': [
                {
                    'course_name': outcome.comments,
                    'course_type': outcome.course_type,
                    'status': outcome.status
                } for outcome in student.outcomes
            ]
        }

        student_data.append(student_dict)

    return jsonify({
        "message": "Students details are retrieved successfully.",
        "status": 200,
        "students": student_data
    }), 200
