from flask import Blueprint, request, jsonify
from models import db, Recommender

recommender_bp = Blueprint('recommender', __name__)

@recommender_bp.route('', methods=['POST'])
def add_recommender():
    data = request.json
    rec = Recommender(
        student_id=data['student_id'],
        name=data.get('name'),
        relationship=data.get('relationship'),
        contact=data.get('contact'),
        remarks=data.get('remarks')
    )
    db.session.add(rec)
    db.session.commit()
    return jsonify({"message": "Recommender added", "id": rec.id}), 201

@recommender_bp.route('', methods=['GET'])
def get_recommenders():
    records = Recommender.query.all()
    return jsonify([
        {
            "id": r.id,
            "student_id": r.student_id,
            "name": r.name,
            "relationship": r.relationship,
            "contact": r.contact,
            "remarks": r.remarks
        } for r in records
    ])
