from flask import Blueprint, jsonify
from models import db, CourseStatus

status_get_bp = Blueprint('status_get', __name__)

@status_get_bp.route('/api/statusdetails', methods=['GET'])
def get_status_details():
    statuses = CourseStatus.query.all()

    result = []
    total_total_seats = 0
    total_allocated_seats = 0
    total_remaining_seats = 0

    # First: Aided courses
    for status in statuses:
        if status.course_type == "Aided":
            remaining_seats = status.total_seats - status.allocated_seats

            result.append({
                "course": status.course_name,
                "course_type": status.course_type,
                "total_seats": status.total_seats,
                "allocated_seats": status.allocated_seats,
                "remaining_seats": remaining_seats
            })

    # Then: Self-Finance courses
    for status in statuses:
        if status.course_type == "Self Finance":
            remaining_seats = status.total_seats - status.allocated_seats

            result.append({
                "course": status.course_name,
                "course_type": status.course_type,
                "total_seats": status.total_seats,
                "allocated_seats": status.allocated_seats,
                "remaining_seats": remaining_seats
            })

            total_total_seats += status.total_seats
            total_allocated_seats += status.allocated_seats
            total_remaining_seats += remaining_seats

    # Add totals row
    result.append({
        "course": "Total Count",
        "course_type": "",
        "total_seats": total_total_seats,
        "allocated_seats": total_allocated_seats,
        "remaining_seats": total_remaining_seats
    })

    return jsonify(result), 200
