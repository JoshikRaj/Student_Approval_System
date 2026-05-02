from flask import Blueprint, jsonify, request
from sqlalchemy import func
from models import db, TcartsCourseStatus, TcartsAdmissionOutcome
from auth import token_required

tcarts_status_get_bp = Blueprint('tcarts_status_get', __name__, url_prefix='/api/tcarts')

@tcarts_status_get_bp.route('/statusdetails', methods=['GET'])
@token_required
def get_tcarts_status_details(user_id, user_email):
    # Get all course statuses from tcarts tables
    statuses = TcartsCourseStatus.query.all()
    outcome_counts_query = (
        db.session.query(TcartsAdmissionOutcome.status, func.count(TcartsAdmissionOutcome.id))
        .group_by(TcartsAdmissionOutcome.status)
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

    for status in statuses:
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

    # Append SF totals row (Fix typo: 'Self Finanace' → 'Self Finance')
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


@tcarts_status_get_bp.route('/updateseats', methods=['PUT'])
@token_required
def update_tcarts_seats(user_id, user_email):
    """Update TcartsCourseStatus seat totals. Fix 7: validate SF cap."""
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Expected a JSON array of seat update objects'}), 400

    # Validate fields
    for item in data:
        if 'course' not in item or 'course_type' not in item or 'total_seats' not in item:
            return jsonify({'error': 'Each item must have course, course_type, and total_seats'}), 400
        if not isinstance(item['total_seats'], int) or item['total_seats'] < 0:
            return jsonify({'error': f"Invalid total_seats for {item['course']}"}), 400

    # Find SF cap row if supplied
    sf_cap_row = next(
        (item for item in data if item.get('course') == 'Self Finance' and item.get('course_type') == 'Total Count'),
        None
    )

    try:
        for item in data:
            course_name = item['course']
            course_type = item['course_type']
            total_seats = item['total_seats']

            # Skip summary / totals rows
            if course_name in ['Self Finance', 'Total Applications']:
                continue

            course_status = TcartsCourseStatus.query.filter_by(
                course_name=course_name,
                course_type=course_type
            ).first()

            if not course_status:
                return jsonify({'error': f'Course not found: {course_name} ({course_type})'}), 404

            if total_seats < course_status.allocated_seats:
                return jsonify({
                    'error': f'{course_name}: New total ({total_seats}) cannot be less than already allocated seats ({course_status.allocated_seats})'
                }), 400

            course_status.total_seats = total_seats

        # Fix 7: Validate that sum of individual SF courses does not exceed SF Total cap
        all_sf_courses = TcartsCourseStatus.query.filter_by(course_type='Self Finance').all()
        new_sf_sum = sum(c.total_seats for c in all_sf_courses)
        if sf_cap_row is not None:
            cap_value = sf_cap_row.get('total_seats', new_sf_sum)
            if new_sf_sum > cap_value:
                db.session.rollback()
                return jsonify({
                    'error': f'Total individual Self Finance seats ({new_sf_sum}) exceed the SF Total cap ({cap_value}). Please reduce individual course seats.'
                }), 400

        db.session.commit()
        return jsonify({'message': 'TCA seats updated successfully', 'sf_total': new_sf_sum}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
