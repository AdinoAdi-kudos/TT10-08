from flask import Blueprint, render_template, request, redirect, url_for, session
import json
from models import db

app_quiz = Blueprint('app_quiz', __name__)

answer_counts = {'FOM': 0, 'FCM': 0, 'FAC': 0, 'FCA': 0, 'FCI': 0, 'FOE': 0}
result_descriptions = {
    'FOM': 'You are a FOM!',
    'FCM': 'You are a FCM!',
    'FAC': 'You are a FAC!',
    'FCA': 'You are a FCA!',
    'FCI': 'You are a FCI!',
    'FOE': 'You are a FOE!'
}

def read_questions(filename):
    questions = []
    current_question = {'question': '', 'options': {}}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            elif line.startswith('Question'):
                current_question = {'question': line, 'options': {}}
                questions.append(current_question)
            else:
                option, _, rest = line.partition(': ')
                text, _, image = rest.partition(', ')
                answers = [a.strip() for a in option.split(',')]
                current_question['options'][option] = {'text': text.strip(), 'answers': answers, 'image': image.strip()}
    return questions


def read_logged_in_users():
    logged_in_users = {}
    with open('user_results.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            username = parts[0]
            result_description = ', '.join(parts[1:])
            if username in logged_in_users:
                logged_in_users[username]['results'].append(result_description)
            else:
                logged_in_users[username] = {
                    'results': [result_description],
                    'username': username
                }
    return logged_in_users

@app_quiz.route('/quiz1', methods=['GET', 'POST'])
def quiz1():
    questions = read_questions('quiz1.txt')
    if request.method == 'POST':
        if 'answer' in request.form:
            selected_answer = request.form['answer']
            for question in questions:
                for option, data in question['options'].items():
                    if selected_answer == option:
                        for answer in data['answers']:
                            answer_counts[answer] += 1
            return redirect(url_for('app_quiz.quiz2'))
    return render_template('quiz1.html', questions=questions)

@app_quiz.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    questions = read_questions('quiz2.txt')
    if request.method == 'POST':
        if 'answer' in request.form:
            selected_answer = request.form['answer']
            for question in questions:
                for option, data in question['options'].items():
                    if selected_answer == option:
                        for answer in data['answers']:
                            answer_counts[answer] += 1
            return redirect(url_for('app_quiz.quiz3'))
    return render_template('quiz2.html', questions=questions)

@app_quiz.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    questions = read_questions('quiz3.txt')
    if request.method == 'POST':
        if 'answer' in request.form:
            selected_answer = request.form['answer']
            for question in questions:
                for option, data in question['options'].items():
                    if selected_answer == option:
                        for answer in data['answers']:
                            answer_counts[answer] += 1
            return redirect(url_for('app_quiz.quiz4'))
    return render_template('quiz3.html', questions=questions)

@app_quiz.route('/quiz4', methods=['GET', 'POST'])
def quiz4():
    questions = read_questions('quiz4.txt')
    if request.method == 'POST':
        if 'answer' in request.form:
            selected_answer = request.form['answer']
            for question in questions:
                for option, data in question['options'].items():
                    if selected_answer == option:
                        for answer in data['answers']:
                            answer_counts[answer] += 1
                            with open('results.txt', 'a') as f:
                                f.write(f"{answer}: {answer_counts[answer]}\n")
            username = session['username']
            max_answer = max(answer_counts, key=answer_counts.get)
            result_description = result_descriptions[max_answer]
            with open('user_results.txt', 'a') as f:
                f.write(f"{username}, {result_description['description']}\n")
            return redirect(url_for('app_quiz.results'))
    return render_template('quiz4.html', questions=questions)

with open('results_descriptions.json') as f:
    result_descriptions = json.load(f)

@app_quiz.route('/results', methods=['GET'])
def results():
    max_answer = max(answer_counts, key=answer_counts.get)
    result_description = result_descriptions[max_answer]
    result_count = answer_counts[max_answer]

    username = session['username']

    logged_in_users = read_logged_in_users()
    user_results = [res for res in logged_in_users.get(username, {}).get('results', [])]

    different_results = [res[0] for res in user_results if res[0]!= result_description]

    similar_result_count = 0
    with open('user_results.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(', ')
            user_result = parts[1:]
            if result_description['description'] in user_result:
                similar_result_count += 1
                
    total_users = sum(1 for line in open('user_results.txt'))
    if total_users == 0:
        pick_rate = 0
    else:
        pick_rate = (similar_result_count / total_users) * 100

    similar_result_users = []
    with open('user_results.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(', ')
            user_result = parts[1:]
            if result_description['description'] in user_result:
                similar_result_users.append(parts[0])
                print("Similar result count:", similar_result_count)

    return render_template('results.html', 
                        result_description=result_description, 
                        similar_result_count=similar_result_count,
                        result_count=result_count, 
                        username=username, 
                        different_results=different_results, 
                        pick_rate=pick_rate,
                        user_results=user_results,
                        logged_in_users=logged_in_users,
                        similar_result_users=similar_result_users)

if __name__ == '__main__':
    app = Blueprint(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    app.register_blueprint(app_quiz)
    app.run(debug=True)
