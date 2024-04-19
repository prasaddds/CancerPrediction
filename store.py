from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

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

        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            return 'Username already exists. Please choose a different username.'
        elif existing_email:
            return 'Email already exists. Please use a different email address.'
        elif password != confirm_password:
            return 'Passwords do not match. Please try again.'
        else:
            # Create a new user object
            new_user = User(username=username, email=email, password=password)

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided username exists in the database
        user = User.query.filter_by(username=username).first()

        # If user exists and password matches, redirect to home page
        if user and user.password == password:
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def home():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    arr = np.array([[data1, data2, data3, data4]])
    pred = model.predict(arr)
    return render_template('after.html', data=pred)

if __name__ == "__main__":
    app.run(debug=True)
