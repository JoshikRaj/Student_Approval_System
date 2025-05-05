from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class AdmissionForm(FlaskForm):
    name = StringField("Student Name", validators=[DataRequired()])
    school = StringField("School", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    address = TextAreaField("Address", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    email = StringField("Student Email", validators=[DataRequired(), Email()])
    marks = TextAreaField("12th Marks", validators=[DataRequired()])
    cutoff = FloatField("Engineering Cutoff", validators=[DataRequired()])
    aadhar = StringField("Aadhar Number", validators=[DataRequired()])
    income = StringField("Annual Income", validators=[DataRequired()])
    branches = StringField("Branches Opted (comma separated)", validators=[DataRequired()])
    date_applied = StringField("Date of Application", validators=[DataRequired()])
    recommender_name = StringField("Recommender Name", validators=[DataRequired()])
    recommender_designation = StringField("Designation", validators=[DataRequired()])
    recommender_office = StringField("Office Name", validators=[DataRequired()])
    recommender_phone = StringField("Phone", validators=[DataRequired()])
    submit = SubmitField("Submit Application")
