from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Student model (minimal for FK)
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)

# Define YearOfPassing model
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

# Create tables
with app.app_context():
    db.create_all()

# ---------------- API ROUTES ----------------

@app.route('/api/year-of-passing', methods=['GET'])
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

@app.route('/api/year-of-passing', methods=['POST'])
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

@app.route('/api/year-of-passing/<int:id>', methods=['PUT'])
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

@app.route('/api/year-of-passing/<int:id>', methods=['DELETE'])
def delete_year_of_passing(id):
    record = YearOfPassing.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Year of Passing deleted"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
