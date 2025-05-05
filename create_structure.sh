#!/bin/bash

mkdir -p college_admission_app/templates
mkdir -p college_admission_app/static

touch college_admission_app/app.py
touch college_admission_app/config.py
touch college_admission_app/models.py
touch college_admission_app/forms.py
touch college_admission_app/requirements.txt
touch college_admission_app/static/style.css

touch college_admission_app/templates/login.html
touch college_admission_app/templates/staff_form.html
touch college_admission_app/templates/admin_dashboard.html

echo "✅ Flask project scaffold created!"
