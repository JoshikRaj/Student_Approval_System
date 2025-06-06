from flask import Blueprint, send_file, jsonify
from io import BytesIO
import pandas as pd
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from models import db, Student, Recommender, AdmissionOutcome, TcartsStudent, TcartsRecommender, TcartsAdmissionOutcome
from constants import APPROVED, DECLINED, ONHOLD, WITHDRAWN, UNALLOCATED

exports_bp = Blueprint('exports', __name__)

@exports_bp.route('/api/exports', methods=['GET'])
def export_students():
    # Define status values and convert to lowercase for matching
    valid_statuses = [APPROVED, DECLINED, ONHOLD, WITHDRAWN, UNALLOCATED]
    valid_statuses_lower = [status.lower() for status in valid_statuses]

    # ---------------- TCE STUDENTS ----------------
    tce_students = Student.query.options(
        joinedload(Student.recommenders),
        joinedload(Student.outcomes)
    ).filter(
        func.lower(Student.outcomes.status).in_(valid_statuses_lower)
    ).all()

    tce_data = []
    for student in tce_students:
        outcome = student.outcomes[0] if student.outcomes else None
        recommender = student.recommenders[0] if student.recommenders else None
        tce_data.append({
            "College": "TCE",
            "ID": student.id,
            "Name": student.name,
            "Application Number": student.application_number,
            "School": student.school,
            "District": student.district,
            "Cut Off": float(student.engineering_cutoff) if student.engineering_cutoff else None,
            "Twelfth Mark": student.twelfth_mark,
            "Application Status": student.applicationstatus,
            "Email": student.email,
            "Community": student.community,
            "Mark %": float(student.markpercentage) if student.markpercentage else None,
            "Degree Type": getattr(student, 'degreeType', None),
            "Degree": student.degree,
            "Course": student.branch_1,
            "Recommender Name": recommender.name if recommender else None,
            "Recommender Email": recommender.email if recommender else None,
            "Admission Status": outcome.status if outcome else None,
            "Course Type": outcome.course_type if outcome else None,
        })

    # ---------------- TCARTS STUDENTS ----------------
    tcarts_students = TcartsStudent.query.options(
        joinedload(TcartsStudent.recommenders),
        joinedload(TcartsStudent.outcomes)
    ).filter(
        func.lower(TcartsStudent.outcomes.status).in_(valid_statuses_lower)
    ).all()

    tcarts_data = []
    for student in tcarts_students:
        outcome = student.outcomes[0] if student.outcomes else None
        recommender = student.recommenders[0] if student.recommenders else None
        tcarts_data.append({
            "College": "TCARTS",
            "ID": student.id,
            "Name": student.name,
            "Application Number": student.application_number,
            "School": student.school,
            "District": student.district,
            "Cut Off": float(student.cutoff) if student.cutoff else None,
            "Twelfth Mark": student.twelfth_mark,
            "Application Status": student.applicationstatus,
            "Email": student.email,
            "Community": student.community,
            "Mark %": None,
            "Degree Type": student.degreeType,
            "Degree": student.degree,
            "Course": student.course,
            "Recommender Name": recommender.name if recommender else None,
            "Recommender Email": recommender.email if recommender else None,
            "Admission Status": outcome.status if outcome else None,
            "Course Type": outcome.course_type if outcome else None,
        })

    # Combine both data
    combined_data = tce_data + tcarts_data

    if not combined_data:
        return jsonify({"message": "No students found with the selected statuses."}), 404

    # Create DataFrame and write to Excel
    df = pd.DataFrame(combined_data)
    output = BytesIO()
    
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Students')
        output.seek(0)

        return send_file(
            output,
            download_name="student_export.xlsx",
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({"error": f"Failed to generate Excel file: {str(e)}"}), 500