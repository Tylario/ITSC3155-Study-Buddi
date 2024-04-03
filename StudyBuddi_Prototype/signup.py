from flask import Flask, render_template

app = Flask(__name__)

@app.route('/signup')
def match():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)