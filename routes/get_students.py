# routes/student_routes.py
from flask import Blueprint, jsonify
from models import db, Student, Recommender

get_students_bp = Blueprint('get_students', __name__)

@get_students_bp.route('/api/students', methods=['GET'])
def get_students_by_cutoff():
    try:
        # Fetch students who have a non-null engineering_cutoff
        students = Student.query.filter(Student.engineering_cutoff.isnot(None)).all()

        # Sort by branch_1 (department) ascending, then by cutoff descending
        students.sort(key=lambda s: (s.branch_1 or "", -float(s.engineering_cutoff)))

        result = []
        for student in students:
            recommenders = [
                {
                    "name": r.name,
                    "designation": r.designation,
                    "email": r.email,
                    "affiliation": r.affiliation,
                    "personal_phone_number": r.personal_phone_number,
                    "office_phone_number": r.office_phone_number,
                    "office_address": r.office_address,
                    "offcode": r.offcode,
                    "percode": r.percode
                }
                for r in student.recommenders
            ]

            result.append({
                "id": student.id,
                "name": student.name,
                "aadhar_number": student.aadhar_number,
                "application_number": student.application_number,
                "engineering_cutoff": float(student.engineering_cutoff),
                "email": student.email,
                "phone_number": student.phone_number,
                "date_of_application": student.date_of_application.isoformat() if student.date_of_application else None,
                "applicationstatus": student.applicationstatus,
                "degree": student.degree,
                "college": student.college,
                "district": student.district,
                "community": student.community,
                "board": student.board,
                "school": student.school,
                "branch_1": student.branch_1,
                "branch_2": student.branch_2,
                "branch_3": student.branch_3,
                "year_of_passing": student.year_of_passing,
                "markpercentage": student.markpercentage,
                "twelfth_mark": student.twelfth_mark,
                "maths": student.maths,
                "physics": student.physics,
                "chemistry": student.chemistry,
                "parent_annual_income": str(student.parent_annual_income),
                "stdcode": student.stdcode,
                "studybreak": student.studybreak,
                "recommenders": recommenders
            })

        return jsonify({
            "message": "Students retrieved successfully.",
            "status": 200,
            "students": result
        })

    except Exception as e:
        return jsonify({
            "message": "Error retrieving students.",
            "status": 500,
            "error": str(e)
        })
