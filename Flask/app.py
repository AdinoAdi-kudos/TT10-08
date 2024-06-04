from flask import Flask, render_template, request, redirect, url_for, session

from flask import Blueprint

app_quiz = Blueprint('app_quiz', __name__, template_folder='templates')

#from flask import Blueprint, render_template, request, redirect, url_for

#app_quiz = Blueprint('app_quiz', __name__)

answer_counts = {'FOM': 0, 'FCM': 0, 'FAC': 0, 'FCA': 0, 'FCI': 0, 'FOE': 0}

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
            return redirect(url_for('app_quiz.results'))
    return render_template('quiz4.html', questions=questions)

@app_quiz.route('/results', methods=['GET'])
def results():
    return render_template('results.html', answer_counts=answer_counts)

if __name__ == '__main__':
    app_quiz.run(debug=True)