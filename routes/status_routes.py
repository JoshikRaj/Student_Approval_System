from flask import Blueprint, jsonify
from models import db, CourseStatus, Student

status_get_bp = Blueprint('status_get', __name__)

@status_get_bp.route('/api/statusdetails', methods=['GET'])
def get_status_details():
    # Get all course statuses
    statuses = CourseStatus.query.all()

    result = []
    for status in statuses:
        remaining_seats = status.total_seats - status.allocated_seats

        result.append({
            "course": status.course_name,
            "course_type": status.course_type,
            "total_seats": status.total_seats,
            "allocated_seats": status.allocated_seats,
            "remaining_seats": remaining_seats
        })

    return jsonify(result), 200
