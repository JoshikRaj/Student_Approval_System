from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Minimal Student model for foreign key
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)

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

# Create tables
with app.app_context():
    db.create_all()

# ---------------- API ROUTES ----------------

@app.route('/api/recommenders', methods=['GET'])
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

@app.route('/api/recommenders', methods=['POST'])
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

@app.route('/api/recommenders/<int:id>', methods=['PUT'])
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

@app.route('/api/recommenders/<int:id>', methods=['DELETE'])
def delete_recommender(id):
    record = Recommender.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Recommender deleted"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
