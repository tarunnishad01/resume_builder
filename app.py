from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from fpdf import FPDF
import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/template-preview')
def template_preview():
    return render_template('template_preview.html')

# Route for the home page (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route for the templates page
@app.route('/templates')
def templates_page():
    return render_template('template.html')

# Route for the about page
@app.route('/about')
def about_page():
    return render_template('about.html')

# Route for the contact page
@app.route('/contact')
def contact_page():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('index.html', title="Resume Builder")

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        summary = request.form.get('summary')

        # Handle file upload
        profile_photo = None
        if 'photo-upload' in request.files:
            file = request.files['photo-upload']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                profile_photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(profile_photo)

        # Collect experiences and education
        experiences = []
        educations = []

        for key, value in request.form.items():
            if key.startswith('job-title-'):
                index = key.split('-')[-1]
                experiences.append({
                    'job_title': value,
                    'company': request.form.get(f'company-{index}'),
                    'start_date': request.form.get(f'start-date-{index}'),
                    'end_date': request.form.get(f'end-date-{index}'),
                    'description': request.form.get(f'job-description-{index}')
                })
            elif key.startswith('degree-'):
                index = key.split('-')[-1]
                educations.append({
                    'degree': value,
                    'institution': request.form.get(f'institution-{index}'),
                    'start_date': request.form.get(f'edu-start-date-{index}'),
                    'end_date': request.form.get(f'edu-end-date-{index}')
                })

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Resume: {first_name} {last_name}", ln=True, align='C')

        pdf.cell(0, 10, ln=True)
        pdf.cell(0, 10, txt=f"Email: {email}, Phone: {phone}", ln=True)
        pdf.cell(0, 10, txt=f"Address: {address}", ln=True)

        pdf.cell(0, 10, ln=True)
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt="Professional Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=summary)

        pdf.cell(0, 10, ln=True)
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt="Work Experience", ln=True)
        pdf.set_font("Arial", size=12)
        for exp in experiences:
            pdf.cell(0, 10, txt=f"{exp['job_title']} at {exp['company']} ({exp['start_date']} - {exp['end_date']})", ln=True)
            pdf.multi_cell(0, 10, txt=exp['description'])

        pdf.cell(0, 10, ln=True)
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt="Education", ln=True)
        pdf.set_font("Arial", size=12)
        for edu in educations:
            pdf.cell(0, 10, txt=f"{edu['degree']} at {edu['institution']} ({edu['start_date']} - {edu['end_date']})", ln=True)

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{first_name}_{last_name}_resume.pdf")
        pdf.output(pdf_path)

        return send_file(pdf_path, as_attachment=True)

    return render_template('\Templates\index.html')


if __name__ == '__main__':
    app.run(debug=True)
