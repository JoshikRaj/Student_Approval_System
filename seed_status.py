from flask import Flask
from models import db, CourseStatus
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
# Use correct path if your DB is in a different folder
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# List of departments / courses at TCE
course_names = [
    "B.E. Civil Engineering",
    "B.E. Mechanical Engineering",
    "B.E. Electrical and Electronics Engineering",
    "B.E. Electronics and Communication Engineering",
    "B.E. Computer Science and Engineering",
    "B.Tech. Information Technology",
    "B.E. Mechatronics",
    "B.Tech. Computer Science and Business Systems",
    "B.E. Computer Science and Engineering (AI & ML)",
    "B.Des. Interior Design",
    "B.Arch. Architecture",
    "Msc. Data Science",
]

course_types = ["Aided", "Self Finance"]

with app.app_context():
    try:
        db.create_all()

        for name in course_names:
            for ctype in course_types:
                exists = CourseStatus.query.filter_by(course_name=name, course_type=ctype).first()
                if not exists:
                    new_course = CourseStatus(
                        course_name=name,
                        course_type=ctype,
                        total_seats=20,
                        allocated_seats=0
                    )
                    db.session.add(new_course)
                    print(f"✅ Added: {name} ({ctype})")
                else:
                    print(f"ℹ️ Already exists: {name} ({ctype})")

        db.session.commit()
        print("🎉 Courses seeded successfully.")

    except Exception as e:
        db.session.rollback()
        print("❌ Error while seeding courses:", e)
