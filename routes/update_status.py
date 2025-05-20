from flask import Blueprint, request, jsonify
from models import db, AdmissionOutcome,CourseStatus, Student
from constants import APPROVED, DECLINED, ONHOLD,UNALLOCATED  # Make sure ONHOLD is imported

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/updatestatus', methods=['PUT'])
def update_status():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')
    course_name = data.get('course')
    course_type = data.get('course_type')

    if not student_id or status not in [APPROVED, DECLINED, ONHOLD,UNALLOCATED] :
        return jsonify({'error': 'Invalid input'}), 400

    outcome = AdmissionOutcome.query.filter_by(student_id=student_id).first()
    if not outcome:
        return jsonify({'error': 'Student outcome not found'}), 404

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    old_status = outcome.status

    # Update selected student's status
    outcome.status = status
    if status == APPROVED:
        outcome.course_type = course_type
        outcome.comments = course_name  # Ideally, use a dedicated course_name column

        # Handle seat updates only if the status changed
        course_status = CourseStatus.query.filter_by(
            course_name=course_name,
            course_type=course_type
        ).first()

        if not course_status:
            return jsonify({'error': 'Course not found'}), 404

    if old_status != status:
        if status == APPROVED:
            if course_status.allocated_seats < course_status.total_seats:
                course_status.allocated_seats += 1
            else:
                return jsonify({"error": "No seats available"}), 400
        # elif old_status == APPROVED and status != APPROVED:
        #     if course_status.allocated_seats > 0:
        #         course_status.allocated_seats -= 1

    # 🧠 Reject other students with same Aadhar number
    if status == APPROVED:
        other_students = Student.query.filter(
            Student.aadhar_number == student.aadhar_number,
            Student.id != student_id
        ).all()

        for other in other_students:
            other_outcome = AdmissionOutcome.query.filter_by(student_id=other.id).first()
            if other_outcome and other_outcome.status != DECLINED:
                other_outcome.status = DECLINED
                other_outcome.comments = 'Already allocated'

    db.session.commit()

    return jsonify({
        'message': f'Status updated to {status} for student {student_id}',
    }), 200
