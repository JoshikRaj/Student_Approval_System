from flask import Blueprint, request, jsonify
from models import db, AdmissionOutcome, Student
from constants import APPROVED, DECLINED, ONHOLD  # Make sure ONHOLD is imported

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/updatestatus', methods=['PUT'])
def update_status():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')
    course = data.get('course')
    course_type = data.get('course_type')

    if not student_id or status not in [APPROVED, DECLINED, ONHOLD] or not course or not course_type:
        return jsonify({'error': 'Invalid input'}), 400

    outcome = AdmissionOutcome.query.filter_by(student_id=student_id).first()
    if not outcome:
        return jsonify({'error': 'Student outcome not found'}), 404

    # Update fields
    outcome.status = status
    outcome.course_type = course_type  # already exists in your model
    outcome.comments = course          # storing course name in comments or consider adding course_name column

    db.session.commit()
    return jsonify({'message': f'Status updated to {status} with course {course} ({course_type}) for student {student_id}'}), 200
