from flask import Blueprint, render_template, request, redirect, url_for

app_quiz = Blueprint('quiz', __name__)

answer_counts = {'FOM': 0, 'FCM': 0, 'FAC': 0, 'FCA': 0, 'FCI': 0, 'FOE': 0}

@app_quiz.route('/quiz1', methods=['GET', 'POST'])
def quiz1():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('quiz.quiz2'))
    return render_template('quiz1.html')

@app_quiz.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('quiz.quiz3'))
    return render_template('quiz2.html')

@app_quiz.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('quiz.quiz4'))
    return render_template('quiz3.html')

@app_quiz.route('/quiz4', methods=['GET', 'POST'])
def quiz4():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('quiz.results'))
    return render_template('quiz4.html')

@app_quiz.route('/results')
def results():
    return render_template('results.html', answer_counts=answer_counts, reset_url=url_for('quiz.reset'))

@app_quiz.route('/reset')
def reset():
    global answer_counts
    answer_counts = {'FOM': 0, 'FCM': 0, 'FAC': 0, 'FCA': 0, 'FCI': 0, 'FOE': 0}
    return redirect(url_for('quiz.quiz1'))