from flask import Blueprint, render_template, request, redirect, url_for

quiz_blueprint = Blueprint('quiz', __name__)

@quiz_blueprint.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        # Process quiz answers and calculate score
        score = 0
        for question in quiz_questions:
            answer = request.form[question['id']]
            if answer == question['correct_answer']:
                score += 1
        return render_template('quiz_result.html', score=score)
    return render_template('quiz.html', questions=quiz_questions)

quiz_questions = [
    {'id': 'q1', 'question': 'What is the capital of France?', 'correct_answer': 'Paris'},
]