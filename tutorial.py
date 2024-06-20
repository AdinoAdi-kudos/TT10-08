from flask import Flask, render_template, request, redirect, url_for, session
from app import app_quiz
from models import db, User

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'TT10-08'
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(app_quiz, url_prefix='/quiz')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        with open('users.txt', 'r') as f:
            existing_users = [line.strip().split(', ')[0].split(': ')[1] for line in f.readlines()]
            if username in existing_users:
                return render_template('register.html', message='Username already exists. Please choose a different username.')

        with open('users.txt', 'a') as f:
            f.write(f"Username: {username}, Password: {password}, Email: {email}\n")

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('users.txt', 'r') as f:
            for line in f.readlines():
                user_data = line.strip().split(', ')
                if user_data[0].split(': ')[1] == username and user_data[1].split(': ')[1] == password:
                    session['username'] = username
                    with open('logged_in_users.txt', 'a') as f:
                        f.write(f"{username}\n")
                    return redirect(url_for('app_quiz.quiz1'))

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
        user = User.query.filter_by(username=username).first()
        if user and user.password == old_password:
            user.password = new_password
            db.session.commit()
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
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('delete_password.html', message='Incorrect password. Please try again.')
    return render_template('delete_password.html')

if __name__ == '__main__':
    app.run(debug=True)
