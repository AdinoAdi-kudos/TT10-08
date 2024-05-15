from flask import Blueprint, render_template, request, redirect, url_for

quiz_blueprint = Blueprint('quiz', __name__)

# Use a dictionary to store the scores, instead of separate variables
scores = {'FOE': 0, 'FCI': 0, 'FOM': 0, 'FAC': 0, 'FCM': 0}

@quiz_blueprint.route('/q1', methods=['GET', 'POST'])
def q1():
    if request.method == 'POST':
        q1s = request.form['q1s']
        if q1s == "Yes":
            global scores
            scores['FOE'] += 1
            scores['FCI'] += 1
            scores['FOM'] += 0
            scores['FAC'] -= 1
            scores['FCM'] -= 1
        elif q1s == "No":
            global scores
            scores['FOE'] -= 1
            scores['FCI'] -= 1
            scores['FOM'] += 0
            scores['FAC'] += 1
            scores['FCM'] += 1
        return redirect(url_for('foe.q2'))
    return render_template('q1.html')

@quiz_blueprint.route('/q2')
def q2():
    # implement q2 logic here
    pass