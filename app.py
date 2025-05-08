from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from routes.students import student_bp
from routes.recommender import recommender_bp
from routes.admission_outcome import outcome_bp
from routes.get_students import get_students_bp  # ← ADD THIS
from routes.login import login_bp 
from routes.registration import registration_bp 
from routes.update_status import status_bp 

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/api/students')
app.register_blueprint(recommender_bp, url_prefix='/api/recommenders')
app.register_blueprint(outcome_bp, url_prefix='/api/outcomes')
app.register_blueprint(status_bp)
app.register_blueprint(get_students_bp) 
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)# ← REGISTER HERE (no url_prefix needed since it's already in the route)
@app.route('/')
def home():
    return "Student Approval System API is running!"

if __name__ == '__main__':
    app.run(debug=True)
