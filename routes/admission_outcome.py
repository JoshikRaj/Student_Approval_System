from flask import Blueprint, request, jsonify
from models import db, AdmissionOutcome
from datetime import datetime

outcome_bp = Blueprint('admission_outcome', __name__)

@outcome_bp.route('', methods=['POST'])
def add_outcome():
    data = request.json
    current_year = str(datetime.now().year)
    outcome = AdmissionOutcome(
        student_id=data['student_id'],
        status=data.get('status'),
        year_of_admission=current_year
    )
    db.session.add(outcome)
    db.session.commit()
    return jsonify({"message": "Admission outcome recorded", "id": outcome.id}), 201

@outcome_bp.route('', methods=['GET'])
def get_outcomes():
    current_year = str(datetime.now().year)
    records = AdmissionOutcome.query.filter(AdmissionOutcome.year_of_admission == current_year).all()
    return jsonify([
        {
            "id": r.id,
            "student_id": r.student_id,
            "status": r.status
        } for r in records
    ])
