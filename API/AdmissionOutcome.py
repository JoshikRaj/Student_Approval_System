from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Minimal Student model for FK reference
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)

# AdmissionOutcome model
class AdmissionOutcome(db.Model):
    __tablename__ = 'admission_outcomes'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    degree = db.Column(String)
    department = db.Column(String)      # Recommended department
    status = db.Column(String)          # e.g., 'Allotted', 'Rejected', etc.
    branch_allotted = db.Column(String) # Final branch allotted if status is Allotted

# Create tables
with app.app_context():
    db.create_all()

# ---------------- API ROUTES ----------------

@app.route('/api/admission-outcomes', methods=['GET'])
def get_admission_outcomes():
    records = AdmissionOutcome.query.all()
    return jsonify([
        {
            "id": r.id,
            "student_id": r.student_id,
            "degree": r.degree,
            "department": r.department,
            "status": r.status,
            "branch_allotted": r.branch_allotted
        } for r in records
    ])

@app.route('/api/admission-outcomes', methods=['POST'])
def add_admission_outcome():
    data = request.json
    record = AdmissionOutcome(
        student_id=data['student_id'],
        degree=data.get('degree'),
        department=data.get('department'),
        status=data.get('status'),
        branch_allotted=data.get('branch_allotted')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Admission outcome added", "id": record.id}), 201

@app.route('/api/admission-outcomes/<int:id>', methods=['PUT'])
def update_admission_outcome(id):
    data = request.json
    record = AdmissionOutcome.query.get_or_404(id)

    record.degree = data.get('degree', record.degree)
    record.department = data.get('department', record.department)
    record.status = data.get('status', record.status)
    record.branch_allotted = data.get('branch_allotted', record.branch_allotted)

    db.session.commit()
    return jsonify({"message": "Admission outcome updated"})

@app.route('/api/admission-outcomes/<int:id>', methods=['DELETE'])
def delete_admission_outcome(id):
    record = AdmissionOutcome.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Admission outcome deleted"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
