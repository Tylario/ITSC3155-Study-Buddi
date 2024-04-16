from __future__ import print_function
import sys
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import uuid


app = Flask(__name__)
app.secret_key = 'BzukLhBXWv1Gs8xILzN2Wg6qofvbsUJy'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    major = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    studynotes = db.Column(db.Text, nullable=True)
    class1 = db.Column(db.String(50), nullable=True)
    class2 = db.Column(db.String(50), nullable=True)
    class3 = db.Column(db.String(50), nullable=True)
    class4 = db.Column(db.String(50), nullable=True)
    class5 = db.Column(db.String(50), nullable=True)
    #pfp = db.Column(db.LargeBinary, nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()
    sample_user = User(username='testuser', password='testpassword',name='name', email = 'testemail', major = 'testmajor', bio = 'testbio', studynotes = 'teststudynotes', class1 = 'testclass1', class2 = 'testclass2', class3 = 'testclass3', class4 = 'testclass4', class5 = 'testclass5')
    db.session.add(sample_user)
    # db.session.commit()

@app.route('/')
def index():
    user_in_session = session.get('user')
    return render_template('index.html', user=user_in_session)

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_user = session['user']
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        bio = request.form.get('bio')
        class1 = request.form.get('class1')
        # Add other form fields as needed
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            user.name = name
            user.email = email
            user.bio = bio
            user.class1 = class1
            db.session.commit()
        # Update user's information in the database

        return render_template('match.html',user = user)
    
    return render_template('profile.html')

@app.route('/updateProfile', methods=['GET','POST'])
def updateProfile():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        current_user = session['user']
        user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        current_user = session['user']
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        bio = request.form.get('bio')
        class1 = request.form.get('class1')
        # Add other form fields as needed
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            user.name = name
            user.email = email
            user.bio = bio
            user.class1 = class1
            db.session.commit()
        # Update user's information in the database

        return render_template('match.html', user=user)
    return render_template('updateProfile.html', user = user)

@app.route('/match')
def match():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    all_users = User.query.all()
    users_json = [{
        'name': user.name,
        'email': user.email,
        'major': user.major or "",  # Provide default empty string if None
        'class1': user.class1 or "",
        'class2': user.class2 or "",
        'class3': user.class3 or "",
        'class4': user.class4 or "",
        'class5': user.class5 or "",
        'bio': user.bio or "",
        'img': user.img if user.img else 'https://via.placeholder.com/150'  # Default placeholder image
    } for user in all_users]

    return render_template('match.html', allUsers=users_json)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('match'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Store the user in session
            session['user'] = user
            return redirect(url_for('updateProfile',user = user))

        # Render the login page with an error message if login fails
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('match'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            # Render the signup page with an error message if the username already exists
            return render_template('signup.html', error='Username already exists')

        # Create a new User object with the provided data
        new_user = User(username=username, password=password)
        session['user'] = new_user
        # Add the new user to the database session
        db.session.add(new_user)
        db.session.commit()

        # Store the new user in session
        session['user'] = new_user
        return render_template('profile.html')

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
