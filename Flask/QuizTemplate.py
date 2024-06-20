from flask import Blueprint, render_template, request, redirect, url_for

quiz_blueprint = Blueprint('quiz', __name__)

# Use a dictionary to store the scores, instead of separate variables
scores = {'FOE': 0, 'FCI': 0, 'FOM': 0, 'FAC': 0, 'FCM': 0}

@quiz_blueprint.route('/q1', methods=['GET', 'POST'])
def q1():
    global scores
    if request.method == 'POST':
        q1s = request.form['q1s']
        if q1s == "Yes":
            scores['FOE'] += 1
            scores['FCI'] += 1
            scores['FOM'] += 0
            scores['FAC'] -= 1
            scores['FCM'] -= 1
        elif q1s == "No":
            scores['FOE'] -= 1
            scores['FCI'] -= 1
            scores['FOM'] += 0
            scores['FAC'] += 1
            scores['FCM'] += 1
        return redirect(url_for('quiz.q2'))
    
    with open('quiz1.txt', 'r') as f:
        lines = f.readlines()
        question = lines[0].strip()
        options = {}
        for line in lines[1:]:
            option_data = line.strip().split(': ')
            option_keys = option_data[0].split(', ')
            option_text = option_data[1]
            for option_key in option_keys:
                options[option_key] = {'text': option_text}
                
    return render_template('q1.html', question=question, options=options)

@quiz_blueprint.route('/q2')
def q2():
    # implement q2 logic here
    pass