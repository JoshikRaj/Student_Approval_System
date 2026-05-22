import pandas as pd
from datetime import datetime

from app import app
from models import db, Student, Recommender, AdmissionOutcome

EXCEL_FILE = "data.xlsx"


def normalize(value):
    if pd.isna(value):
        return None
    return str(value).strip()


with app.app_context():

    try:
        df = pd.read_excel(EXCEL_FILE)

        inserted = 0
        skipped = 0

        for index, row in df.iterrows():

            try:
                application_number = normalize(row.get("application_number"))

                if not application_number:
                    print(f"Row {index+2}: Missing application number")
                    skipped += 1
                    continue

                # Duplicate check
                existing = Student.query.filter_by(
                    application_number=application_number
                ).first()

                if existing:
                    print(f"Row {index+2}: Duplicate {application_number}")
                    skipped += 1
                    continue

                degree = normalize(row.get("degree"))
                program_type = normalize(row.get("program_type"))

                if degree:
                    degree = degree.lower()

                if program_type:
                    program_type = program_type.lower()

                # Auto detect program type
                pg_degrees = ['me_mtech', 'march', 'mca']
                ug_degrees = ['btech', 'be', 'msc', 'bdes', 'barch']

                if not program_type:
                    if degree in pg_degrees:
                        program_type = 'pg'
                    elif degree in ug_degrees:
                        program_type = 'ug'

                # Date conversion
                date_of_application = datetime.utcnow()

                if pd.notna(row.get('date_of_application')):
                    date_of_application = pd.to_datetime(
                        row.get('date_of_application')
                    )

                student = Student(
                    application_number=application_number,
                    name=normalize(row.get('name')),
                    school=normalize(row.get('school')),
                    district=normalize(row.get('district')),
                    address=normalize(row.get('address')),
                    stdcode=normalize(row.get('stdcode')),
                    phone_number=normalize(row.get('phone_number')),
                    email=normalize(row.get('email')),
                    aadhar_number=normalize(row.get('aadhar_number')),
                    parent_annual_income=row.get('parent_annual_income'),
                    community=normalize(row.get('community')),
                    college=normalize(row.get('college')),
                    degree=degree,
                    program_type=program_type,

                    ug_consolidated_mark=row.get('ug_consolidated_mark'),
                    ug_course_name=normalize(row.get('ug_course_name')),
                    ug_institution=normalize(row.get('ug_institution')),
                    tancet_gate_score=row.get('tancet_gate_score'),

                    branch_1=normalize(row.get('branch_1')),
                    branch_2=normalize(row.get('branch_2')),
                    branch_3=normalize(row.get('branch_3')),

                    board=normalize(row.get('board')),

                    maths=row.get('maths'),
                    physics=row.get('physics'),
                    chemistry=row.get('chemistry'),

                    nata=row.get('nata'),
                    msc_cutoff=row.get('msc_cutoff'),
                    barch_cutoff=row.get('barch_cutoff'),
                    bdes_cutoff=row.get('bdes_cutoff'),

                    applicationstatus=normalize(row.get('applicationstatus')),

                    twelfth_mark=row.get('twelfth_mark'),
                    markpercentage=row.get('markpercentage'),
                    engineering_cutoff=row.get('engineering_cutoff'),

                    year_of_passing=row.get('year_of_passing'),

                    diploma_cgpa=row.get('diploma_cgpa'),
                    diploma_college_name=normalize(row.get('diploma_college_name')),
                    diploma_course=normalize(row.get('diploma_course')),
                    diploma_university=normalize(row.get('diploma_university')),

                    lateral_cutoff=row.get('lateral_cutoff'),

                    date_of_application=date_of_application,
                    year_of_admission=str(datetime.now().year)
                )

                db.session.add(student)
                db.session.flush()

                # Recommender
                recommender_name = normalize(row.get('recommender_name'))

                if recommender_name:

                    recommender = Recommender(
                        student_id=student.id,
                        name=recommender_name,
                        designation=normalize(row.get('recommender_designation')),
                        affiliation=normalize(row.get('recommender_affiliation')),
                        office_address=normalize(row.get('recommender_office_address')),
                        offcode=normalize(row.get('recommender_offcode')),
                        office_phone_number=normalize(row.get('recommender_office_phone_number')),
                        percode=normalize(row.get('recommender_percode')),
                        personal_phone_number=normalize(row.get('recommender_personal_phone_number')),
                        email=normalize(row.get('recommender_email'))
                    )

                    db.session.add(recommender)

                # Admission outcome
                admission = AdmissionOutcome(
                    student_id=student.id,
                    status='UNALLOCATED',
                    year_of_admission=str(datetime.now().year)
                )

                db.session.add(admission)

                inserted += 1

                print(f"Inserted: {application_number}")

            except Exception as row_error:
                print(f"Row {index+2} failed: {row_error}")

        db.session.commit()

        print("\n========== IMPORT COMPLETE ==========")
        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")

    except Exception as e:
        db.session.rollback()
        print("IMPORT FAILED")
        print(str(e))
