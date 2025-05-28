from flask import Blueprint, request, jsonify
from models import db, TcartsAdmissionOutcome, CourseStatus, TcartsStudent
from constants import APPROVED, DECLINED, ONHOLD, UNALLOCATED, WITHDRAWN, DELETE

tcarts_status_bp = Blueprint('tcarts_status', __name__, url_prefix='/api/tcarts')

@tcarts_status_bp.route('/updatestatus', methods=['PUT'])
def update_tcarts_status():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')
    course_name = data.get('course')
    course_type = data.get('course_type')
    is_confirm = data.get('is_confirm')

    if not student_id or status not in [APPROVED, DECLINED, ONHOLD, UNALLOCATED, WITHDRAWN, DELETE]:
        return jsonify({'error': 'Invalid input for status'}), 400

    outcome = TcartsAdmissionOutcome.query.filter_by(student_id=student_id).first()
    if not outcome:
        return jsonify({'error': 'Student outcome not found'}), 404

    student = TcartsStudent.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student details not found'}), 404

    old_status = outcome.status
    old_name = outcome.comments if old_status == APPROVED else None
    old_type = outcome.course_type if old_status == APPROVED else None

    # Update status and comments
    outcome.status = status
    if status == DECLINED:
        outcome.comments = course_name

    if status == APPROVED or old_status == APPROVED:
        outcome.course_type = course_type
        outcome.comments = course_name

        course_status = None
        if old_status == APPROVED:
            course_status = CourseStatus.query.filter_by(
                course_name=old_name,
                course_type=old_type
            ).first()
        else:
            course_status = CourseStatus.query.filter_by(
                course_name=course_name,
                course_type=course_type
            ).first()

        if not course_status:
            return jsonify({'error': 'Course not found'}), 404

    # Update allocated seats only if status changed
    if old_status != status:
        if status == APPROVED:
            if course_status.allocated_seats < course_status.total_seats:
                course_status.allocated_seats += 1
            else:
                return jsonify({"error": "No seats available"}), 400
        elif old_status == APPROVED and status != APPROVED:
            if course_status.allocated_seats > 0:
                course_status.allocated_seats -= 1

    # Reject other students with same Aadhar number if this student is approved
    if status == APPROVED:
        other_students = TcartsStudent.query.filter(
        TcartsStudent.id != student_id,
        TcartsStudent.date_of_birth == student.date_of_birth,
        TcartsStudent.twelfth_mark == student.twelfth_mark,
        TcartsStudent.year_of_passing == student.year_of_passing,
        TcartsStudent.phone_number == student.phone_number,
        (TcartsStudent.subject1 + TcartsStudent.subject2 + TcartsStudent.subject3 + TcartsStudent.subject4) ==
        (student.subject1 + student.subject2 + student.subject3 + student.subject4)
    ).all()
        for other in other_students:
            other_outcome = TcartsAdmissionOutcome.query.filter_by(student_id=other.id).first()
            if other_outcome and other_outcome.status == APPROVED:
                if not is_confirm:
                    return jsonify({'error': 'This student has already been allotted a seat, do you want to change the allotment?'}), 409

                other_course_status = CourseStatus.query.filter_by(
                    course_name=other_outcome.comments,
                    course_type=other_outcome.course_type
                ).first()
                if other_course_status and other_course_status.allocated_seats > 0:
                    other_course_status.allocated_seats -= 1

                other_outcome.status = DECLINED
                other_outcome.comments = 'This student has already been allotted a course.'

    db.session.commit()

    return jsonify({
        'message': f'Application status updated to {status} for student {student.name}'
    }), 200
