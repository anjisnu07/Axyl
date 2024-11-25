from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/doctor')
def dr():
    return render_template('doctor_survey.html')

@app.route('/patient')
def patient():
    return render_template('patient_survey.html')

if __name__ == '__main__':
    app.run(debug=True)
