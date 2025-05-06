from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, ForeignKey
from flask import Blueprint

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- Models ----------------

# Student model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)

# YearOfPassing model
class YearOfPassing(db.Model):
    __tablename__ = 'year_of_passing'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    medium = db.Column(String)
    mark_mathematics = db.Column(Integer)
    mark_physics = db.Column(Integer)
    mark_chemistry = db.Column(Integer)
    engg_cutoff = db.Column(DECIMAL)
    break_of_study = db.Column(Boolean)

# Recommender model
class Recommender(db.Model):
    __tablename__ = 'recommenders'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    name = db.Column(String)
    designation = db.Column(String)
    affiliation = db.Column(String)
    office_address = db.Column(Text)
    office_phone = db.Column(String)
    personal_phone = db.Column(String)
    email = db.Column(String)

# AdmissionOutcome model
class AdmissionOutcome(db.Model):
    __tablename__ = 'admission_outcomes'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(Integer, ForeignKey('students.id'), nullable=False)
    degree = db.Column(String)
    department = db.Column(String)      # Recommended department
    status = db.Column(String)          # e.g., 'Allotted', 'Rejected', etc.
    branch_allotted = db.Column(String) # Final branch allotted if status is Allotted

# ---------------- API Blueprints ----------------

# Year of Passing Blueprint
year_of_passing_bp = Blueprint('year_of_passing', __name__)

@year_of_passing_bp.route('/api/year-of-passing', methods=['GET'])
def get_year_of_passing():
    records = YearOfPassing.query.all()
    return jsonify([
        {
            "id": r.id,
            "student_id": r.student_id,
            "medium": r.medium,
            "mark_mathematics": r.mark_mathematics,
            "mark_physics": r.mark_physics,
            "mark_chemistry": r.mark_chemistry,
            "engg_cutoff": float(r.engg_cutoff),
            "break_of_study": r.break_of_study
        } for r in records
    ])

@year_of_passing_bp.route('/api/year-of-passing', methods=['POST'])
def add_year_of_passing():
    data = request.json
    record = YearOfPassing(
        student_id=data['student_id'],
        medium=data.get('medium'),
        mark_mathematics=data.get('mark_mathematics'),
        mark_physics=data.get('mark_physics'),
        mark_chemistry=data.get('mark_chemistry'),
        engg_cutoff=data.get('engg_cutoff'),
        break_of_study=data.get('break_of_study', False)
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Year of Passing added", "id": record.id}), 201

@year_of_passing_bp.route('/api/year-of-passing/<int:id>', methods=['PUT'])
def update_year_of_passing(id):
    data = request.json
    record = YearOfPassing.query.get_or_404(id)

    record.medium = data.get('medium', record.medium)
    record.mark_mathematics = data.get('mark_mathematics', record.mark_mathematics)
    record.mark_physics = data.get('mark_physics', record.mark_physics)
    record.mark_chemistry = data.get('mark_chemistry', record.mark_chemistry)
    record.engg_cutoff = data.get('engg_cutoff', record.engg_cutoff)
    record.break_of_study = data.get('break_of_study', record.break_of_study)

    db.session.commit()
    return jsonify({"message": "Year of Passing updated"})

@year_of_passing_bp.route('/api/year-of-passing/<int:id>', methods=['DELETE'])
def delete_year_of_passing(id):
    record = YearOfPassing.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Year of Passing deleted"})


# Recommender Blueprint
recommender_bp = Blueprint('recommender', __name__)

@recommender_bp.route('/api/recommenders', methods=['GET'])
def get_recommenders():
    records = Recommender.query.all()
    return jsonify([
        {
            "id": r.id,
            "student_id": r.student_id,
            "name": r.name,
            "designation": r.designation,
            "affiliation": r.affiliation,
            "office_address": r.office_address,
            "office_phone": r.office_phone,
            "personal_phone": r.personal_phone,
            "email": r.email
        } for r in records
    ])

@recommender_bp.route('/api/recommenders', methods=['POST'])
def add_recommender():
    data = request.json
    record = Recommender(
        student_id=data['student_id'],
        name=data.get('name'),
        designation=data.get('designation'),
        affiliation=data.get('affiliation'),
        office_address=data.get('office_address'),
        office_phone=data.get('office_phone'),
        personal_phone=data.get('personal_phone'),
        email=data.get('email')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Recommender added", "id": record.id}), 201

@recommender_bp.route('/api/recommenders/<int:id>', methods=['PUT'])
def update_recommender(id):
    data = request.json
    record = Recommender.query.get_or_404(id)

    record.name = data.get('name', record.name)
    record.designation = data.get('designation', record.designation)
    record.affiliation = data.get('affiliation', record.affiliation)
    record.office_address = data.get('office_address', record.office_address)
    record.office_phone = data.get('office_phone', record.office_phone)
    record.personal_phone = data.get('personal_phone', record.personal_phone)
    record.email = data.get('email', record.email)

    db.session.commit()
    return jsonify({"message": "Recommender updated"})

@recommender_bp.route('/api/recommenders/<int:id>', methods=['DELETE'])
def delete_recommender(id):
    record = Recommender.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Recommender deleted"})


# Admission Outcome Blueprint
admission_outcome_bp = Blueprint('admission_outcome', __name__)

@admission_outcome_bp.route('/api/admission-outcomes', methods=['GET'])
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

@admission_outcome_bp.route('/api/admission-outcomes', methods=['POST'])
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

@admission_outcome_bp.route('/api/admission-outcomes/<int:id>', methods=['PUT'])
def update_admission_outcome(id):
    data = request.json
    record = AdmissionOutcome.query.get_or_404(id)

    record.degree = data.get('degree', record.degree)
    record.department = data.get('department', record.department)
    record.status = data.get('status', record.status)
    record.branch_allotted = data.get('branch_allotted', record.branch_allotted)

    db.session.commit()
    return jsonify({"message": "Admission outcome updated"})

@admission_outcome_bp.route('/api/admission-outcomes/<int:id>', methods=['DELETE'])
def delete_admission_outcome(id):
    record = AdmissionOutcome.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Admission outcome deleted"})

# Register Blueprints
app.register_blueprint(year_of_passing_bp)
app.register_blueprint(recommender_bp)
app.register_blueprint(admission_outcome_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
