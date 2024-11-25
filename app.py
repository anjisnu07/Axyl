from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model for storing responses
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    concern = db.Column(db.String(100), nullable=False)
    doctorVisit = db.Column(db.String(100), nullable=False)
    technology = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<SurveyResponse {self.name}>"

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/doctor')
def dr():
    return render_template('doctor_survey.html')

@app.route('/patient')
def patient():
    return render_template('patient_survey.html')


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    concern = db.Column(db.String(500))
    doctorVisit = db.Column(db.String(500))
    technology = db.Column(db.String(500))

    def __repr__(self):
        return f"<Feedback {self.id}>"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')  # Use your HTML form template here

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    concern = ', '.join(request.form.getlist('concern[]'))
    doctorVisit = ', '.join(request.form.getlist('doctorVisit[]'))
    technology = ', '.join(request.form.getlist('technology[]'))
    
    # Validate form data
    if not name or not phone or not email:
        return "Please fill out all required fields.", 400
    
    # Add the feedback to the database
    new_feedback = Feedback(
        name=name, 
        phone=phone, 
        email=email, 
        concern=concern, 
        doctorVisit=doctorVisit, 
        technology=technology
    )
    db.session.add(new_feedback)
    db.session.commit()

    return redirect(url_for('sub'))

@app.route('/feedback-988318166')
def feedback():
    # Query all feedback records from the Feedback table
    feedback_records = Feedback.query.all()
    
    # Return the feedback data to the feedback.html template
    return render_template('feedback.html', feedback_records=feedback_records)

@app.route('/Thank-you')
def sub():
    return render_template('form-submitted.html')
if __name__ == '__main__':
    app.run(debug=True)
