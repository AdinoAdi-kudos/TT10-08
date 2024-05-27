from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

answer_counts = {'FOM': 0, 'FCM': 0, 'FAC': 0, 'FCA': 0, 'FCI': 0, 'FOE': 0}

@app.route('/', methods=['GET', 'POST'])
def quiz1():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('quiz2'))
    return render_template('quiz1.html')

@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('quiz3'))
    return render_template('quiz2.html')

@app.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if request.method == 'POST':
        selected_answer = request.form['answer']
        answer_counts[selected_answer] += 1
        return redirect(url_for('results'))
    return render_template('quiz3.html')

@app.route('/results')
def results():
    return render_template('results.html', answer_counts=answer_counts)

if __name__ == '__main__':
    app.run()
