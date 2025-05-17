from models import db, User, Student, Recommender
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

admin_email = "abs@gmail.com"
admin_password = "abc123"

other_users = [
    {"email": "user1@example.com", "password": "pass1", "isadmin": "yes"},
    {"email": "user2@example.com", "password": "pass2", "isadmin": "no"},
    {"email": "user3@example.com", "password": "pass3", "isadmin": "no"}
]

students_data = [
    {
        "application_number": "APP1234",
        "name": "John Doe",
        "school": "XYZ High School",
        "district": "ABC District",
        "address": "123 Street, City",
        "stdcode": "STD001",
        "phone_number": "1234567890",
        "email": "johndoe@example.com",
        "aadhar_number": "1234-5678-9012",
        "parent_annual_income": 500000.00,
        "community": "General",
        "college": "XYZ College",
        "degree": "BTech",
        "branch_1": "Computer Science",
        "branch_2": "Mathematics",
        "branch_3": "Physics",
        "board": "CBSE",
        "maths": 90.5,
        "physics": 85.0,
        "chemistry": 80.0,
        "nata": 150.5,
        "studybreak": 1,
        "msc_cutoff": 90.0,
        "barch_cutoff": 85.0,
        "bdes_cutoff": 80.0,
        "twelfth_mark": 85,
        "markpercentage": 87.5,
        "engineering_cutoff": 88.0,
        "date_of_application": "2025-05-12",
        "applicationstatus": "Pending",
        "year_of_passing": "2025"
    }
]

recommenders_data = [
    {
        "student_application_number": "APP1234",
        "name": "Dr. Smith",
        "designation": "Professor",
        "affiliation": "XYZ College",
        "office_address": "123 College St.",
        "offcode": "044",
        "office_phone_number": "9876543210",
        "percode": "044",
        "personal_phone_number": "9988776655",
        "email": "dr.smith@xyzcollege.com"
    }
]

with app.app_context():
    db.create_all()

    # Admin user
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(email=admin_email)
        db.session.add(admin_user)

    admin_user.is_admin = True
    admin_user.password_hash = generate_password_hash(admin_password)

    # Other users
    for u in other_users:
        user = User.query.filter_by(email=u["email"]).first()
        if not user:
            user = User(email=u["email"])
            db.session.add(user)
        user.is_admin = u["isadmin"].lower() == "yes"
        user.password_hash = generate_password_hash(u["password"])

    # Students
    for student_data in students_data:
        # Convert date string to datetime.date object
        if isinstance(student_data.get("date_of_application"), str):
            student_data["date_of_application"] = datetime.strptime(
                student_data["date_of_application"], "%Y-%m-%d"
            ).date()

        # Check if student exists
        student = Student.query.filter_by(application_number=student_data["application_number"]).first()
        if not student:
            student = Student(**student_data)

            db.session.add(student)
        else:
            for key, value in student_data.items():
                setattr(student, key, value)


    db.session.flush()  # ensure student IDs are available for recommender FK use

    # Recommenders
    for recommender_data in recommenders_data:
        student_app_num = recommender_data.pop("student_application_number")
        student = Student.query.filter_by(application_number=student_app_num).first()
        if not student:
            continue  # skip if student doesn't exist
        recommender = Recommender.query.filter_by(student_id=student.id).first()
        if not recommender:
            recommender = Recommender(student_id=student.id, **recommender_data)
            db.session.add(recommender)
        else:
            for key, value in recommender_data.items():
                setattr(recommender, key, value)

    db.session.commit()
    print("Users, students, and recommenders created or updated successfully.")
