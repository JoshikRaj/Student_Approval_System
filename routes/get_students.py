from flask import Blueprint, jsonify, request
from models import Student, AdmissionOutcome, Recommender
from sqlalchemy.orm import joinedload


from flask import Blueprint, jsonify, request
from models import Student, AdmissionOutcome, Recommender
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, desc

get_students_bp = Blueprint('get_students', __name__)

from sqlalchemy import case

def get_sort_key(student):
    degree = (student.degree or "").lower()
    
    # Primary sort by degree
    degree_order = {
        'be': 1, 'btech': 1, 'b.e': 1, 'b.tech': 1,  # Group all BE/BTech together
        'msc': 2,
        'barch': 3,
        'bdes': 4
    }
    degree_value = degree_order.get(degree, 999)  # Unknown degrees sort last
    
    # Secondary sort by the relevant cutoff
    cutoff_value = None
    if degree in ['be', 'btech', 'b.e', 'b.tech']:
        cutoff_value = student.engineering_cutoff if student.college == 'TCE' else None
    elif degree == 'msc':
        cutoff_value = student.msc_cutoff
    elif degree == 'barch':
        cutoff_value = student.barch_cutoff
    elif degree == 'bdes':
        cutoff_value = student.bdes_cutoff
    
    # Convert None to a large negative number so nulls sort last
    cutoff_value = cutoff_value if cutoff_value is not None else float('-inf')
    
    # Return a tuple for sorting (degree first, then cutoff in descending order)
    return (degree_value, -cutoff_value)  # Negative for descending order

# Sort the students list

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
    

    students = query.all()
    students.sort(key=get_sort_key)
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
            ],
           'outcomes': [
                {
                    'course_name': outcome.comments,
                    'course_type': outcome.course_type
                } for outcome in student.outcomes
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