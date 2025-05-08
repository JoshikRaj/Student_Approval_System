from flask import Blueprint, request, jsonify
from models import db, AdmissionOutcome, Student
from constants import APPROVED, DECLINED

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/updatestatus', methods=['PUT'])
def update_status():
    data = request.get_json()
    student_id = data.get('student_id')
    status = data.get('status')

    if not student_id or status not in ['APPROVED', 'DECLINED','ONHOLD']:
        return jsonify({'error': 'Invalid input'}), 400

    outcome = AdmissionOutcome.query.filter_by(student_id=student_id).first()
    if not outcome:
        return jsonify({'error': 'Student outcome not found'}), 404

    # Map status string to internal constants
    outcome.status = status 

    db.session.commit()
    return jsonify({'message': f'Status updated to {outcome.status} for student {student_id}'}), 200
