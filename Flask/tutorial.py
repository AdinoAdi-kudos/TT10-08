from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import app as app_quiz_blueprint

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

app.register_blueprint(app_quiz_blueprint.app_quiz, url_prefix='/quiz')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

users = {
    'user1': ['password1', 'user1@example.com'],
    'user2': ['password2', 'user2@example.com'],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        with open('users.txt', 'a') as f:
            f.write(f"Username: {username}, Password: {password}, Email: {email}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = {}
    with open('users.txt', 'r') as f:
        for line in f:
            username, password, email = line.strip().split(', ')
            username = username.split(': ')[1]
            password = password.split(': ')[1]
            email = email.split(': ')[1]
            users[username] = [password, email]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username][0] == password:
            session['username'] = username
            return redirect(url_for('app_quiz.quiz1'))
        else:
            return render_template('login.html', message='Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if users[username][0] == old_password:
            users[username][0] = new_password
            return redirect(url_for('logout'))
        else:
            return render_template('change_password.html', message='Incorrect old password. Please try again.')
    return render_template('change_password.html')

@app.route('/delete_password', methods=['GET', 'POST'])
def delete_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        password = request.form['password']
        if users[username][0] == password:
            del users[username]
            return redirect(url_for('index'))
        else:
            return render_template('delete_password.html', message='Incorrect password. Please try again.')
    return render_template('delete_password.html')


if __name__ == '__main__':
    app.run(debug=True)
