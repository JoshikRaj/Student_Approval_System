
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # ← Add this
from models import db
from routes.students import student_bp
from routes.recommender import recommender_bp
from routes.admission_outcome import outcome_bp
from routes.get_students import get_students_bp
from routes.login import login_bp 
from routes.registration import registration_bp 
from routes.update_status import status_bp 
from routes.status_routes import status_get_bp
from routes.get_students_tcarts import tcarts_students_bp   
from routes.status_tcarts import tcarts_status_get_bp
from routes.students_tcarts import tcarts_student_bp
from routes.update_status_tcarts import tcarts_status_bp

import os
app = Flask(__name__)

CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)
migrate = Migrate(app, db)  # ← Add this

# Do NOT use db.create_all() when using Flask-Migrate

# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/api/students')
app.register_blueprint(recommender_bp, url_prefix='/api/recommenders')
app.register_blueprint(outcome_bp, url_prefix='/api/outcomes')
app.register_blueprint(status_bp)
app.register_blueprint(get_students_bp) 
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(status_get_bp)
app.register_blueprint(tcarts_students_bp)
app.register_blueprint(tcarts_status_get_bp)
app.register_blueprint(tcarts_student_bp)
app.register_blueprint(tcarts_status_bp)

@app.route('/')
def home():
    return "Student Approval System API is running!"

if __name__ == '__main__':
    app.run(debug=True)
import os
print("Connected database path:", os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')))
print("Resolved DB path:", os.path.abspath('students.db'))
