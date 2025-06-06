from flask import Blueprint, jsonify
from sqlalchemy import func
from models import db, CourseStatus,AdmissionOutcome

status_get_bp = Blueprint('status_get', __name__)

@status_get_bp.route('/api/statusdetails', methods=['GET'])
def get_status_details():
    statuses = CourseStatus.query.all()
    outcome_counts_query = (
        db.session.query(AdmissionOutcome.status, func.count(AdmissionOutcome.id))
        .group_by(AdmissionOutcome.status)
        .all()
    )

    counts_dict = {status: count for status, count in outcome_counts_query}
    final_counts = {
        "approved": counts_dict.get("APPROVED", 0),
        "unallocated": counts_dict.get("UNALLOCATED", 0),
        "declined": counts_dict.get("DECLINED", 0),
        "onhold": counts_dict.get("ONHOLD", 0)
    }
    

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
        "course": "Self Finance",
        "course_type": "Total Count",
        "total_seats": total_total_seats,
        "allocated_seats": total_allocated_seats,
        "remaining_seats": total_remaining_seats
    })
    total_count=final_counts["approved"]+final_counts["unallocated"]+final_counts["declined"]+final_counts["onhold"]
    result.append({
        "course": "Total Applications",
        "course_type": "Received",
        "total_seats": total_count ,
        "allocated_seats": final_counts["approved"],
        "remaining_seats": total_count-final_counts["approved"]
    })

    return jsonify(result), 200
