from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from models import db, AdmissionOutcome, CourseStatus, Student
from constants import APPROVED, DECLINED, ONHOLD, UNALLOCATED, WITHDRAWN, DELETE

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/updatestatus', methods=['PUT'])
def update_status():
    data = request.get_json() or {}
    student_id = data.get('student_id')
    status = data.get('status')
    course_name = data.get('course_name') or data.get('course')
    course_type = data.get('course_type')
    is_confirm = data.get('is_confirm')

    if not student_id or status not in [APPROVED, DECLINED, ONHOLD, UNALLOCATED, WITHDRAWN, DELETE]:
        return jsonify({'error': 'Invalid input for status'}), 400

    outcome = AdmissionOutcome.query.filter_by(student_id=student_id).first()
    if not outcome:
        return jsonify({'error': 'Student outcome not found'}), 404

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student details not found'}), 404

    old_status = outcome.status
    old_name = outcome.comments if old_status == APPROVED else None
    old_type = outcome.course_type if old_status == APPROVED else None

    outcome.status = status
    if status == DECLINED:
        outcome.comments = course_name

    # adjust seat counts when approval changes
    if status == APPROVED or old_status == APPROVED:
        if status == APPROVED:
            outcome.course_type = course_type
            outcome.comments = course_name
            course_status = CourseStatus.query.filter_by(
                course_name=course_name,
                course_type=course_type
            ).first()

            if not course_status:
                return jsonify({'error': 'Course not found'}), 404

            if course_type == "Aided":
                if course_status.total_seats <= 0:
                    return jsonify({'error': 'Course Seats Filled Already'}), 404
            if course_type == "Self Finance":
                if course_status.total_seats <= 0 and not is_confirm:
                    return jsonify({'error': 'Course Seats Filled Already'}), 409

            course_status.allocated_seats += 1
            course_status.total_seats -= 1

        if old_status == APPROVED:
            old_course_status = CourseStatus.query.filter_by(
                course_name=old_name,
                course_type=old_type
            ).first()
            if old_course_status and old_course_status.allocated_seats > 0:
                old_course_status.allocated_seats -= 1
                old_course_status.total_seats += 1

    # Note: duplicate-check skipped for main Student model (fields differ from TcartsStudent)

    db.session.commit()

    return jsonify({
        'message': f'Application status updated to {status} for student {student.name}'
    }), 200
