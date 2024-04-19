from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np

# Load the machine learning model
model = pickle.load(open('final.pkl', 'rb'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Move db.create_all() inside the application context
with app.app_context():
    db.create_all()

@app.route('/')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            return 'Username already exists. Please choose a different username.'
        elif existing_email:
            return 'Email already exists. Please use a different email address.'
        elif password != confirm_password:
            return 'Passwords do not match. Please try again.'
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

import numpy as np

# Define medication recommendations based on probability thresholds
def get_medication_recommendation(probabilities):
    if probabilities[0, 0] > 0.7:
        return "High-risk probability. Consider aggressive treatment such as surgery or radiation therapy."
    elif probabilities[0, 1] > 0.5:
        return "Moderate-risk probability. Hormone therapy may be considered."
    else:
        return "Low-risk probability. Active surveillance or watchful waiting may be appropriate."

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extracting and converting input values to float
        radius = float(request.form['radius'])
        texture = float(request.form['texture'])
        perimeter = float(request.form['perimeter'])
        area = float(request.form['area'])
        smoothness = float(request.form['smoothness'])

        # Creating a feature array
        features = np.array([[radius, texture, perimeter, area, smoothness]])

        # Making prediction and obtaining probabilities using the model
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)

        # Get medication recommendation based on probabilities
        medication_recommendation = get_medication_recommendation(probabilities)

        # Rendering the result template with the prediction, probabilities, and medication recommendation
        return render_template('after.html', data=prediction, probabilities=probabilities, medication=medication_recommendation)

    except ValueError:
        # Handling case where non-numeric input is provided
        return "Invalid input. Please enter numeric values for all fields."

# Define a route to see all users
@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('users.html', users=users)

# Define route for About page
@app.route('/about')
def about():
    return render_template('about.html')

# Define route for Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)