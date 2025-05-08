from flask import Blueprint, request, jsonify
from models import db, AdmissionOutcome

outcome_bp = Blueprint('admission_outcome', __name__)

@outcome_bp.route('', methods=['POST'])
def add_outcome():
    data = request.json
    outcome = AdmissionOutcome(
        student_id=data['student_id'],
        status=data.get('status'),
        approved_branch=data.get('approved_branch'),
        remarks=data.get('remarks')
    )
    db.session.add(outcome)
    db.session.commit()
    return jsonify({"message": "Admission outcome recorded", "id": outcome.id}), 201

@outcome_bp.route('', methods=['GET'])
def get_outcomes():
    records = AdmissionOutcome.query.all()
    return jsonify([
        {
            "id": r.id,
            "student_id": r.student_id,
            "status": r.status,
            "approved_branch": r.approved_branch,
            "remarks": r.remarks
        } for r in records
    ])
