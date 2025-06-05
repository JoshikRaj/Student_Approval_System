from flask import Blueprint, request, jsonify
from models import db, TcartsAdmissionOutcome, TcartsCourseStatus, TcartsStudent
from constants import APPROVED, DECLINED, ONHOLD, UNALLOCATED, WITHDRAWN, DELETE
from sqlalchemy import or_

tcarts_status_bp = Blueprint('tcarts_status', __name__, url_prefix='/api/tcarts')

@tcarts_status_bp.route('/updatestatus', methods=['PUT'])
def update_tcarts_status():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')
    course_name = data.get('course_name')
    course_type = data.get('course_type')
    is_confirm = data.get('is_confirm')
    print(f"Looking for course_name='{course_name}', course_type='{course_type}'")
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

    if status == APPROVED or old_status==APPROVED:
        if status==APPROVED:
            outcome.course_type = course_type
            outcome.comments = course_name  # Ideally, use a dedicated course_name column
            course_status = TcartsCourseStatus.query.filter_by(
                course_name=course_name,
                course_type=course_type
            ).first()
            if(course_type == "Aided"):
                if course_status.allocated_seats == course_status.total_seats:
                    return jsonify({'error': 'Course Seats Filled Already'}), 404
            if not course_status:
                return jsonify({'error': 'Course not found'}), 404
            course_status.allocated_seats += 1

        if old_status==APPROVED :
            print(old_name,old_type)
            old_course_status = TcartsCourseStatus.query.filter_by(
            course_name=old_name,
            course_type=old_type
        ).first()
            old_course_status.allocated_seats -= 1

        # Handle seat updates only if the status changed
        
            
    if status == APPROVED:
        other_students = TcartsStudent.query.filter(
        TcartsStudent.id != student_id,
        TcartsStudent.cutoff == student.cutoff,
        TcartsStudent.year == student.year,
        or_(
            TcartsStudent.phone_number == student.phone_number,
             TcartsStudent.phone_number == student.alternate_number,
        ),
        or_(
            TcartsStudent.alternate_number == student.phone_number,
             TcartsStudent.alternate_number == student.alternate_number,
        )   
    ).all()
        for other in other_students:
            other_outcome = TcartsAdmissionOutcome.query.filter_by(student_id=other.id).first()
            if other_outcome and other_outcome.status == APPROVED:
                if not is_confirm:
                    return jsonify({'error': 'This student has already been allotted a seat, do you want to change the allotment?'}), 409

                other_course_status = TcartsCourseStatus.query.filter_by(
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
