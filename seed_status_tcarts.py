from flask import Flask
from models import db, TcartsCourseStatus
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
load_dotenv()
# Use correct path if your DB is in a different folder
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# List of departments / courses from uploaded image
course_data = [
    # Aided Programmes
    ("B.A. Tamil", "Aided"),
    ("B.A. English", "Aided"),
    ("B.A. Economics (Tamil Medium)", "Aided"),
    ("B.Sc. Mathematics", "Aided"),
    ("B.Sc. Physics", "Aided"),
    ("B.Sc. Chemistry", "Aided"),
    ("B.Sc. Botany", "Aided"),
    ("B.Sc. Zoology", "Aided"),
    ("B.Sc. Computer Science", "Aided"),
    ("B.Com.", "Aided"),
    ("B.B.A.", "Aided"),

    # Self-Financed Programmes
    ("B.A. Tamil (English Medium)", "Self Finance"),
    ("B.A. English (English Medium)", "Self Finance"),
    ("B.A. Economics (English Medium)", "Self Finance"),
    ("B.Com. Professional Accounting", "Self Finance"),
    ("B.Com. Computer Applications", "Self Finance"),
    ("B.Com. Honours", "Self Finance"),
    ("B.Com.", "Self Finance"),
    ("B.B.A.", "Self Finance"),
    ("B.C.A.", "Self Finance"),
    ("B.Sc. Mathematics", "Self Finance"),
    ("B.Sc. Physics", "Self Finance"),
    ("B.Sc. Chemistry", "Self Finance"),
    ("B.Sc. Biotechnology", "Self Finance"),
    ("B.Sc. Microbiology", "Self Finance"),
    ("B.Sc. Computer Science", "Self Finance"),
    ("B.Sc. Information Technology", "Self Finance"),
    ("B.Sc. Psychology", "Self Finance"),
    ("B.Sc. Data Science", "Self Finance"),

    # New Programmes
    ("B.Com. (Fintech)", "Self Finance"),
    ("B.Sc. Computer Science in AI", "Self Finance"),
]

# Insert into DB
with app.app_context():
    try:
        db.create_all()
        for name, ctype in course_data:
            exists = TcartsCourseStatus.query.filter_by(course_name=name, course_type=ctype).first()
            if not exists:
                total_seats = 4 if ctype == "Aided" else 6

                new_course = TcartsCourseStatus(
                    course_name=name,
                    course_type=ctype,
                    total_seats=total_seats,
                    allocated_seats=0
                )
                db.session.add(new_course)
                print(f"✅ Added: {name} ({ctype}) with {total_seats} seats")
            else:
                print(f"ℹ️ Already exists: {name} ({ctype})")
        db.session.commit()
        print("🎉 Courses seeded successfully.")
    except Exception as e:
        print(f"❌ Error while seeding courses: {e}")
