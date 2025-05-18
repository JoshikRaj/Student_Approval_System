from flask import Blueprint, request, jsonify
from models import db, AdmissionOutcome,CourseStatus, Student
from constants import APPROVED, DECLINED, ONHOLD  # Make sure ONHOLD is imported

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/updatestatus', methods=['PUT'])
def update_status():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')
    course_name = data.get('course')
    course_type = data.get('course_type')

    if not student_id or status not in [APPROVED, DECLINED, ONHOLD] or not course_name or not course_type:
        return jsonify({'error': 'Invalid input'}), 400

    outcome = AdmissionOutcome.query.filter_by(student_id=student_id).first()
    if not outcome:
        return jsonify({'error': 'Student outcome not found'}), 404

    old_status = outcome.status

    # Update fields
    outcome.status = status
    outcome.course_type = course_type
    outcome.comments = course_name  # better if you add course_name column and use that instead

    course_status = CourseStatus.query.filter_by(
        course_name=course_name,
        course_type=course_type
    ).first()

    if not course_status:
        return jsonify({'error': 'Course not found'}), 404

    # Update seats only if status changed
    if old_status != status:
        # If newly approved, increment allocated seats if possible
        if status == APPROVED:
            if course_status.allocated_seats < course_status.total_seats:
                course_status.allocated_seats += 1
            else:
                return jsonify({"error": "No seats available"}), 400
        # If changing from APPROVED to other status, decrement allocated seats
        elif old_status == APPROVED and status != APPROVED:
            if course_status.allocated_seats > 0:
                course_status.allocated_seats -= 1

    db.session.add(outcome)
    db.session.add(course_status)
    db.session.commit()

    return jsonify({'message': f'Status updated to {status} with course {course_name} ({course_type}) for student {student_id}'}), 200
