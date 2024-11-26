from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure databases for feedback and doctor reviews
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'  # Main feedback database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'dr_review_db': 'sqlite:///dr_feedback.db',  # Doctor review feedback database
}
db = SQLAlchemy(app)

# Define the database model for storing general feedback (in 'feedback.db')
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    concern = db.Column(db.String(500))
    doctorVisit = db.Column(db.String(500))
    technology = db.Column(db.String(500))
    challenge = db.Column(db.String(500))
    booking = db.Column(db.String(500))
    virtual = db.Column(db.String(500))
    priceTransparency = db.Column(db.String(500))
    convenience = db.Column(db.Text)

    def __repr__(self):
        return f"<Feedback {self.id}>"

# Define the database model for storing doctor review feedback (in 'dr_feedback.db')
class DrReviewFeedback(db.Model):
    __bind_key__ = 'dr_review_db'  # Use the 'dr_review_db' database for this model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    challenge = db.Column(db.String(500)) 
    homeboundCare = db.Column(db.String(500))
    remoteCare = db.Column(db.String(500))
    technology = db.Column(db.String(500))
    biggestChallenge = db.Column(db.String(500))
    promotion = db.Column(db.String(500))
    retainingPatients = db.Column(db.String(500))
    usePlatform = db.Column(db.String(500))
    additionalTools = db.Column(db.Text)

    def __repr__(self):
        return f"<DrReviewFeedback {self.id}>"

# Create the database tables (for both Feedback and DrReviewFeedback models)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')  # Main form page

@app.route('/doctor')
def dr():
    return render_template('doctor_survey.html')  # Doctor-specific form page

@app.route('/patient')
def patient():
    return render_template('patient_survey.html')  # Patient-specific form page

# Route for submitting the feedback form (General Feedback)
@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data from the request
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    concern = ', '.join(request.form.getlist('concern[]'))
    doctorVisit = ', '.join(request.form.getlist('doctorVisit[]'))
    technology = ', '.join(request.form.getlist('technology[]'))
    challenge = ', '.join(request.form.getlist('challenge[]'))
    booking = ', '.join(request.form.getlist('booking[]'))
    virtual = ', '.join(request.form.getlist('virtual[]'))
    priceTransparency = ', '.join(request.form.getlist('priceTransparency[]'))
    convenience = request.form.get('convenience')

    # Validate the required fields
    if not name or not phone or not email:
        return "Please fill out all required fields.", 400

    # Save the feedback to the 'feedback.db'
    new_feedback = Feedback(
        name=name,
        phone=phone,
        email=email,
        concern=concern,
        doctorVisit=doctorVisit,
        technology=technology,
        challenge=challenge,
        booking=booking,
        virtual=virtual,
        priceTransparency=priceTransparency,
        convenience=convenience
    )
    db.session.add(new_feedback)
    db.session.commit()

    return redirect(url_for('sub'))  # Redirect to the thank you page

# Route to display all feedback records
@app.route('/feedback-988318166')
def feedback():
    feedback_records = Feedback.query.all()  # Query all feedback from the general feedback table
    return render_template('feedback.html', feedback_records=feedback_records)

# Route for doctor feedback submission
@app.route('/submit_dr', methods=['POST'])
def submit_dr():
    # Get form data for doctor review feedback
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    
    challenges = ', '.join(request.form.getlist('challenge[]'))
    print("Challenges submitted:", challenges)
    homeboundCare = ', '.join(request.form.getlist('homeboundCare[]'))
    remoteCare = ', '.join(request.form.getlist('remoteCare[]'))
    technology = ', '.join(request.form.getlist('technology[]'))
    biggestChallenge = ', '.join(request.form.getlist('biggestChallenge[]'))
    promotion = ', '.join(request.form.getlist('promotion[]'))
    retainingPatients = ', '.join(request.form.getlist('retainingPatients[]'))
    usePlatform = ', '.join(request.form.getlist('usePlatform[]'))
    additionalTools = request.form.get('additionalTools')

    # Validate the required fields
    if not name or not phone or not email:
        return "Please fill out all required fields.", 400

    # Save the doctor review feedback to the 'dr_feedback.db'
    new_dr_feedback = DrReviewFeedback(
        name=name,
        phone=phone,
        email=email,
        challenge=challenges,
        homeboundCare=homeboundCare,
        remoteCare=remoteCare,
        technology=technology,
        biggestChallenge=biggestChallenge,
        promotion=promotion,
        retainingPatients=retainingPatients,
        usePlatform=usePlatform,
        additionalTools=additionalTools
    )
    # Print the values of the new feedback before adding it to the session
    print("Adding new doctor review feedback:")
    print(f"Name: {new_dr_feedback.name}")
    print(f"Phone: {new_dr_feedback.phone}")
    print(f"Email: {new_dr_feedback.email}")
    print(f"Challenges: {new_dr_feedback.challenge}")




    db.session.add(new_dr_feedback)
    db.session.commit()

    return redirect(url_for('sub_dr'))  # Redirect to the thank you page

# Route for doctor feedback records
@app.route('/dr_feedback')
def dr_feedback():
    dr_feedback_records = DrReviewFeedback.query.all()  # Query doctor feedback records
    return render_template('pat.html', feedback_records=dr_feedback_records)

# Thank you page after submitting feedback
@app.route('/Thank-you')
def sub():
    return render_template('form-submitted.html')  # Thank you page for general feedback

# Thank you page for doctor review feedback
@app.route('/Thank-you_dr')
def sub_dr():
    return render_template('form-submitted.html')  # Thank you page for doctor review feedback

if __name__ == '__main__':
    app.run(debug=True)
