from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'  # Use SQLite database for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create the database tables
db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('Username')
        password = request.form.get('password')
        
        # Query the database for the user
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            # Redirect to the profile page if login is successful
            return redirect(url_for('profile'))
        else:
            # If login fails, redirect back to the login page
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    # Render the profile page
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
