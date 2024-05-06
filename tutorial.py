python
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock data for users (username: [password, email])
users = {
    'user1': ['password1', 'user1@example.com'],
    'user2': ['password2', 'user2@example.com'],
    # Add more users as needed
}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username not in users:
            users[username] = [password, email]
            return redirect(url_for('login'))
        else:
            return render_template('register.html', message='Username already exists. Please choose another username.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username][0] == password:
            session['username'] = username
            return redirect(url_for('quiz'))
        else:
            return render_template('login.html', message='Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Rest of the quiz route logic...

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
