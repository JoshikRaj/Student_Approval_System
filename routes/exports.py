from flask import Blueprint, send_file
from io import BytesIO
import pandas as pd
from models import db, Student
from constants import APPROVED, DECLINED, ONHOLD, WITHDRAWN, UNALLOCATED

exports_bp = Blueprint('exports', __name__)

@exports_bp.route('/api/exports', methods=['GET'])
def export_students():
    valid_statuses = [APPROVED, DECLINED, ONHOLD, WITHDRAWN, UNALLOCATED]

    # Query students
    students = Student.query.filter(Student.applicationstatus.in_(valid_statuses)).all()
    print(students)
    # Convert to list of dicts
    student_data = []
    for student in students:
        student_data.append({
            "ID": student.id,
            "Name": student.name,
            "Application_Number":student.application_number,
            'school': student.school,
            'district': student.district,
            "cut_off": student.cutoff,
            'twelfth_mark': student.twelfth_mark,
            'applicationstatus': student.applicationstatus,
            "Email": student.email,
            'community': student.community,
            'markpercentage': student.markpercentage,
            "College": student.college,
            'degreeType': student.degreeType,
            'degree': student.degree,
            'course': student.course,
            
            # Add more fields as needed
        })

    # Convert to DataFrame
    df = pd.DataFrame(student_data)

    # Write to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    output.seek(0)

    # Send as downloadable response
    return send_file(
        output,
        download_name="student_export.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
