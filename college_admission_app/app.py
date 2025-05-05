from flask import Flask, render_template, redirect, request, session
from config import Config
from models import db, Student, Recommender, Status, Department, StudentStatus
from forms import LoginForm, AdmissionForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Dummy credentials
ADMIN_EMAIL = "aabbcc@gmail.com"
PASSWORD = "admin123"

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        if email == ADMIN_EMAIL:
            return redirect('/admin')
        else:
            return redirect(f'/form?email={email}')
    return render_template("login.html", form=form)

@app.route('/form', methods=['GET', 'POST'])
def form():
    email = request.args.get('email')
    form = AdmissionForm()
    if form.validate_on_submit():
        # Store recommender
        recommender = Recommender(
            name=form.recommender_name.data,
            designation=form.recommender_designation.data,
            office_name=form.recommender_office.data,
            phone=form.recommender_phone.data
        )
        db.session.add(recommender)
        db.session.commit()

        # Store student
        student = Student(
            name=form.name.data,
            school=form.school.data,
            district=form.district.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            marks=form.marks.data,
            cutoff=form.cutoff.data,
            aadhar=form.aadhar.data,
            income=form.income.data,
            branches=form.branches.data,
            date_applied=form.date_applied.data,
            recommender_id=recommender.id
        )
        db.session.add(student)
        db.session.commit()
        return "<h2>Application Submitted Successfully!</h2>"
    return render_template("staff_form.html", form=form)

@app.route('/admin')
def admin():
    students = Student.query.all()
    return render_template("admin_dashboard.html", students=students)

@app.route('/status/<int:student_id>', methods=['POST'])
def update_status(student_id):
    status_id = request.form['status']
    student_status = StudentStatus(
        student_id=student_id,
        status_id=status_id,
        department_id=1,  # You can add department selection later
        recommender_id=Student.query.get(student_id).recommender_id
    )
    db.session.add(student_status)
    db.session.commit()
    return redirect('/admin')
