from flask import Blueprint, jsonify, request
from sqlalchemy import func
from models import db, CourseStatus,AdmissionOutcome
from auth import token_required

status_get_bp = Blueprint('status_get', __name__)

@status_get_bp.route('/api/statusdetails', methods=['GET'])
@token_required
def get_status_details(user_id, user_email):
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


@status_get_bp.route('/api/updateseats', methods=['PUT'])
@token_required
def update_seats(user_id, user_email):
    """
    Update total seats for courses.
    
    Request body:
    [
        {
            "course": "B.E. Computer Science and Engineering",
            "course_type": "Aided",
            "total_seats": 100
        },
        ...
    ]
    
    Validates that Self Finance total matches sum of individual SF courses.
    """
    data = request.get_json() or []
    
    if not isinstance(data, list):
        return jsonify({'error': 'Expected a list of updates'}), 400
    
    if len(data) == 0:
        return jsonify({'error': 'No courses provided'}), 400
    
    # Separate SF and Aided updates
    sf_updates = [item for item in data if item.get('course_type', '').lower() == 'self finance']
    aided_updates = [item for item in data if item.get('course_type', '').lower() == 'aided']
    
    # Calculate SF total from direct SF course updates (excluding totals row)
    sf_total = sum(item.get('total_seats', 0) for item in sf_updates 
                   if item.get('course') != 'Self Finance')
    
    # Validate each update has required fields
    for item in data:
        if 'course' not in item or 'course_type' not in item or 'total_seats' not in item:
            return jsonify({'error': 'Each update must have course, course_type, and total_seats'}), 400
        
        if not isinstance(item['total_seats'], int) or item['total_seats'] < 0:
            return jsonify({'error': f"Invalid total_seats for {item['course']}"}), 400
    
    # Update database
    try:
        for item in data:
            course_name = item['course']
            course_type = item['course_type']
            total_seats = item['total_seats']
            
            # Skip total rows
            if course_name in ['Self Finance', 'Total Applications']:
                continue
            
            course_status = CourseStatus.query.filter_by(
                course_name=course_name,
                course_type=course_type
            ).first()
            
            if not course_status:
                return jsonify({'error': f'Course not found: {course_name} ({course_type})'}), 404
            
            # Check if new total would be less than already allocated seats
            if total_seats < course_status.allocated_seats:
                return jsonify({
                    'error': f'{course_name}: New total ({total_seats}) cannot be less than already allocated seats ({course_status.allocated_seats})'
                }), 400
            
            course_status.total_seats = total_seats
        
        db.session.commit()
        
        return jsonify({
            'message': 'Seats updated successfully',
            'sf_total': sf_total
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
