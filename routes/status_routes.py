from flask import Blueprint, jsonify
from models import db, AdmissionOutcome, CourseStatus, Student

status_get_bp = Blueprint('status_get', __name__)

@status_get_bp.route('/api/statusdetails', methods=['GET'])
def get_status_details():
    # Get all student outcomes
    outcomes = AdmissionOutcome.query.all()

    result = []
    for outcome in outcomes:
        student = Student.query.get(outcome.student_id)
        if not student:
            continue

        # Retrieve the course info from comments and course_type fields
        course_name = outcome.comments
        course_type = outcome.course_type

        course_status = CourseStatus.query.filter_by(course_name=course_name, course_type=course_type).first()

        remaining_seats = None
        if course_status:
            remaining_seats = course_status.total_seats - course_status.allocated_seats

        result.append({
            "student_id": student.id,
            "student_name": student.name,
            "course": course_name,
            "course_type": course_type,
            "status": outcome.status,
            "remaining_seats": remaining_seats
        })

    return jsonify(result), 200
