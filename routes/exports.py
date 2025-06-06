from flask import Blueprint, send_file, jsonify
from io import BytesIO
import pandas as pd
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from models import (
    db, Student,
    TcartsStudent,
    CourseStatus, TcartsCourseStatus, AdmissionOutcome, TcartsAdmissionOutcome
)
from constants import APPROVED, DECLINED, ONHOLD, WITHDRAWN, UNALLOCATED

exports_bp = Blueprint('exports', __name__)


@exports_bp.route('/api/exports', methods=['GET'])
def export_students():
    valid_statuses = [APPROVED, DECLINED, ONHOLD, WITHDRAWN, UNALLOCATED]
    valid_statuses_lower = [status.lower() for status in valid_statuses]

    # -- Fetch students --
    def fetch_students(model,OutcomeModel, college_label, is_tce=True):
        students = model.query.options(
            joinedload(model.recommenders),
            joinedload(model.outcomes)
        ).filter(
            model.outcomes.any(
                func.lower(OutcomeModel.status).in_(valid_statuses_lower)
            )
        )

        results = []
        for s in students:
            outcome = s.outcomes[0] if s.outcomes else None
            recommender = s.recommenders[0] if s.recommenders else None
            cutoff_value = (
                s.engineering_cutoff
                or s.msc_cutoff
                or s.barch_cutoff
                or s.cutoff
            ) if is_tce else s.cutoff
            results.append({
                "College": college_label,
                "ID": s.id,
                "Name": s.name,
                "Application Number": s.application_number,
                "School": s.school,
                "Cut Off": float(cutoff_value) if cutoff_value is not None else None,
                "Twelfth Mark": s.twelfth_mark,
                "Email": s.email,
                "Mark %": float(s.markpercentage) if is_tce and s.markpercentage else None,
                "Degree Type": getattr(s, 'degreeType', None),
                "Degree": s.degree,
                "Course": s.branch_1 if is_tce else s.course,
                "Recommender Name": recommender.name if recommender else None,
                "Recommender Email": recommender.email if recommender else None,
                "Admission Status": outcome.status if outcome else None,
                "Course Type": outcome.course_type if outcome else None,
            })
        return results

    students_data = fetch_students(Student,AdmissionOutcome, "TCE", is_tce=True) + fetch_students(TcartsStudent,TcartsAdmissionOutcome, "TCA", is_tce=False)
    df_students = pd.DataFrame(students_data)

    # -- Remaining Seats Sheet --
    def build_remaining( model, college_label):
        expected_list = [
        {
            "course_name": course.course_name,
            "course_type": course.course_type,
            "total_seats": course.total_seats,
            "allocated_seats": course.allocated_seats
        }
        for course in model.query.all()
    ]
        remaining = []
        total_all, allocated_all, remain_all = 0, 0, 0
        for c in expected_list:
            name, ctype, total, allocated = c['course_name'], c['course_type'], c['total_seats'], c['allocated_seats']
            remain = total - allocated
            remaining.append({
                "College": college_label,
                "Course": name,
                "Course Type": ctype,
                "Total Seats": total,
                "Allocated Seats": allocated,
                "Remaining Seats": remain
            })
            if ctype == "Self Finance":
                total_all += total
                allocated_all += allocated
                remain_all += remain
        remaining.append({
            "College": college_label,
            "Course": "Self Finance",
            "Course Type": "Total Count",
            "Total Seats": total_all,
            "Allocated Seats": allocated_all,
            "Remaining Seats": remain_all
        })
        return remaining

    remaining_data = build_remaining(CourseStatus, "TCE") + \
                     build_remaining(TcartsCourseStatus, "TCA")
    df_remaining = pd.DataFrame(remaining_data)

    # -- Write to Excel --
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_students.to_excel(writer, index=False, sheet_name='Students')
        df_remaining.to_excel(writer, index=False, sheet_name='Remaining Seats')

    output.seek(0)
    return send_file(
        output,
        download_name="student_export.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
