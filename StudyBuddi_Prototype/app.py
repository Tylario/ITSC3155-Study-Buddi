from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()
    sample_user = User(id='00', username='testuser', password='testpassword')
    db.session.add(sample_user)
    # db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/match')
def match():
    return render_template('match.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the provided password matches the password in the database
            if user.password == password:
                # Redirect to the profile page if login is successful
                return redirect(url_for('profile'))
        
        # Render the login page with an error message if login fails
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Generate a unique user id
        id = str(uuid.uuid4())

        # Create a new User object with the provided data
        new_user = User(id=id, username=username, password=password)

        # Add the new user to the database session
        db.session.add(new_user)

        # Commit the transaction to save the new user to the database
        db.session.commit()

        # Redirect the user to a success page or render a success message
        return render_template('profile.html')

    # If the request method is GET, simply render the signup.html template
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
