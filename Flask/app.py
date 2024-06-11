from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json


app_quiz = Blueprint('app_quiz', __name__)
db = SQLAlchemy()

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"Result('{self.result}')"

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
                option, _, text = line.partition(': ')
                answers = [a.strip() for a in option.split(',')]
                current_question['options'][option] = {'text': text.strip(), 'answers': answers}
    return questions

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
            return redirect(url_for('app_quiz.results'))
    return render_template('quiz4.html', questions=questions)

with open('results_descriptions.json') as f:
    result_descriptions = json.load(f)

@app_quiz.route('/results', methods=['GET'])
def results():
    max_answer = max(answer_counts, key=answer_counts.get)
    result_description = result_descriptions[max_answer]
    with open('results.txt', 'r') as f:
        for line in f:
            answer, count = line.strip().split(': ')
            if count.isdigit():
                answer_counts[answer] = int(count)
    result_count = answer_counts[max_answer]
    return render_template('results.html', result_description=result_description, result_count=result_count, results_traits=result_description['traits'])

if __name__ == '__main__':
    app = (__name__)
    db.init_app(app)
    app.run(debug=True)