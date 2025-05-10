from flask import Blueprint, jsonify, request
from models import Student, AdmissionOutcome, Recommender
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, desc

get_students_bp = Blueprint('get_students', __name__)

@get_students_bp.route('/api/students', methods=['GET'])
def get_students():
    print("Route /api/students accessed")

    status_filter = request.args.get('status')
    college_filter = request.args.get('college')
    search_query = request.args.get('search')

    # Use eager loading for recommenders
    query = Student.query.options(
        joinedload(Student.recommenders),
        joinedload(Student.outcomes)  # optional, if you want status info
    )

    if status_filter:
        query = query.join(AdmissionOutcome).filter(AdmissionOutcome.status == status_filter)

    if college_filter:
        query = query.filter(Student.college == college_filter)

    if search_query:
        like_pattern = f"%{search_query}%"
        query = query.outerjoin(Recommender).filter(or_(
            Student.name.ilike(like_pattern),
            Student.application_number.ilike(like_pattern),
            Recommender.name.ilike(like_pattern)
        ))

    # Use distinct to avoid duplicates due to joins, but no GROUP BY
    query = query.order_by(desc(Student.engineering_cutoff)).distinct(Student.id)

    students = query.all()

    return jsonify([{
        'id': student.id,
        'application_number': student.application_number,
        'name': student.name,
        'school': student.school,
        'district': student.district,
        'email': student.email,
        'aadhar_number': student.aadhar_number,
        'community': student.community,
        'college': student.college,
        'branch_1': student.branch_1,
        'branch_2': student.branch_2,
        'branch_3': student.branch_3,
        'board': student.board,
        'twelfth_mark': student.twelfth_mark,
        'markpercentage': student.markpercentage,
        'engineering_cutoff': student.engineering_cutoff if student.college == 'TCE' else None,
        'date_of_application': student.date_of_application.strftime('%Y-%m-%d') if student.date_of_application else None,
        'year_of_passing': student.year_of_passing,
        'recommenders': [
            {
                'name': rec.name,
                'designation': rec.designation,
                'affiliation': rec.affiliation,
                'office_address': rec.office_address,
                'office_phone_number': rec.office_phone_number,
                'personal_phone_number': rec.personal_phone_number,
                'email': rec.email
            } for rec in student.recommenders
        ]
    } for student in students])
