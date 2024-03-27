from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('Username')
        password = request.form.get('password')
        
        # redirect to the profile page until logic to validate credentials is added
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    # Here you can render the profile page or perform any other actions
    return render_template('profilepage.html')

if __name__ == '__main__':
    app.run(debug=True)
