from flask import Blueprint, jsonify, request
from models import Student, AdmissionOutcome, Recommender
from sqlalchemy.orm import joinedload


from flask import Blueprint, jsonify, request
from models import Student, AdmissionOutcome, Recommender
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, desc

get_students_bp = Blueprint('get_students', __name__)

from sqlalchemy import case

@get_students_bp.route('/api/students', methods=['GET'])
def get_students():
    print("Route /api/students accessed")

    status_filter = request.args.get('status')
    college_filter = request.args.get('college')
    search_query = request.args.get('search')

    query = Student.query.options(
        joinedload(Student.recommenders),
        joinedload(Student.outcomes)
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

    # Define the case expression for degree-based ordering
    degree_order = case(
        {
            'be': 1, 'btech': 2, 'b.e': 3, 'b.tech': 4,  # BE/BTech comes first
            'msc': 5,                                   # MSC comes second
            'barch': 6, 'bdes': 7                       # BArch and BDes follow
        },
        else_=8  # Anything else will be ordered last
    )

    # Define the cutoff logic based on degree
    cutoff_order = case(
        {
            'be': Student.engineering_cutoff,
            'btech': Student.engineering_cutoff,
            'b.e': Student.engineering_cutoff,
            'b.tech': Student.engineering_cutoff,
            'msc': Student.msc_cutoff,
            'barch': Student.barch_cutoff,
            'bdes': Student.bdes_cutoff
        },
        else_=0  # If degree doesn't match any known type, order by 0
    )

    # Apply custom ordering first by degree and then by cutoff
    query = query.order_by(degree_order, cutoff_order.desc())

    students = query.all()

    student_data = []
    for student in students:
        degree = (student.degree or "").lower()
        is_be_btech = degree in ['be', 'btech', 'b.e', 'b.tech']
        is_msc = degree == 'msc'
        is_barch = degree == 'barch'
        is_bdes = degree == 'bdes'

        student_dict = {
            'id': student.id,
            'application_number': student.application_number,
            'name': student.name,
            'school': student.school,
            'district': student.district,
            'email': student.email,
            'aadhar_number': student.aadhar_number,
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
            ]
        }

        # Add fields conditionally based on degree
        if is_be_btech:
            student_dict.update({
                'maths': student.maths,
                'physics': student.physics,
                'chemistry': student.chemistry,
                'engineering_cutoff': student.engineering_cutoff if student.college == 'TCE' else None
            })
        elif is_msc:
            student_dict['msc_cutoff'] = student.msc_cutoff
        elif is_barch:
            student_dict.update({
                'nata': student.nata,
                'barch_cutoff': student.barch_cutoff
            })
        elif is_bdes:
            student_dict['bdes_cutoff'] = student.bdes_cutoff

        student_data.append(student_dict)

    return jsonify({
        "message": "Students retrieved successfully.",
        "status": 200,
        "students": student_data
    }), 200