from flask import Flask
from models import db, CourseStatus
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
load_dotenv()
# Use correct path if your DB is in a different folder
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
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
    "M.E. Structural Engineering",
    "M.E. Environmental Engineering",
    "M.E. Construction Engineering and Management",
    "M.E. Engineering Design",
    "M.E. Power System Engineering",
    "M.E. Communication Systems",
    "M.E. Computer Science and Engineering",
    "M.Arch. Architecture",
    "MCA"
]

course_types = ["Aided", "Self Finance"]

with app.app_context():
    try:
        db.create_all()

        for name in course_names:
            for ctype in course_types:
                # Skip "Aided" mode for Msc and B.Des
                # Skip "Aided" mode for Msc, B.Des, and all B.Tech. courses
                if (name == "Msc. Data Science" and ctype == "Aided") or \
                (name == "B.Des. Interior Design" and ctype == "Aided") or \
                 (name == "B.E. Mechatronics" and ctype == "Aided") or \
                    (name == "B.E. Computer Science and Engineering (AI & ML)" and ctype == "Aided") or \
                (name.startswith("B.Tech.") and ctype == "Aided") or \
                (name.startswith("M.E.") and ctype == "Aided") or \
                (name == "M.Arch. Architecture" and ctype == "Aided") or \
                (name == "MCA" and ctype == "Aided"):

                    print(f"⚠️ Skipping: {name} ({ctype}) — Not available")
                    continue

                exists = CourseStatus.query.filter_by(course_name=name, course_type=ctype).first()
                if not exists:
                    # Set total seats based on course name and type
                    total_seats = 0

                    if ctype == "Aided":
                        if name == "B.E. Computer Science and Engineering":
                            total_seats = 5
                        elif name == "B.E. Electronics and Communication Engineering":
                            total_seats = 5
                        elif name == "B.E. Electrical and Electronics Engineering":
                            total_seats = 5
                        elif name == "B.E. Civil Engineering":
                            total_seats = 4
                        elif name == "B.E. Mechanical Engineering":
                            total_seats = 5
                        elif name == "B.Arch. Architecture":
                            total_seats = 7
                        else:
                            total_seats = 0  # Just in case

                    elif ctype == "Self Finance":
                        if name in [
                            "B.E. Civil Engineering",
                            "B.E. Mechanical Engineering",
                            "B.E. Electrical and Electronics Engineering",
                            "B.E. Electronics and Communication Engineering",
                            "B.E. Computer Science and Engineering",
                            "B.Tech. Information Technology",
                            "B.E. Mechatronics",
                            "B.Tech. Computer Science and Business Systems",
                            "B.E. Computer Science and Engineering (AI & ML)"
                        ]:
                            total_seats = 12
                        elif name in ["B.Arch. Architecture", "B.Des. Interior Design"]:
                            total_seats = 10
                        elif name == "Msc. Data Science":
                            total_seats = 4
                        elif name.startswith("M.E."):
                            total_seats = 10
                        elif name == "M.Arch. Architecture":
                            total_seats = 10
                        elif name == "MCA":
                            total_seats = 10

                    new_course = CourseStatus(
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
