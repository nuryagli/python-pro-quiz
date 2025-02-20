from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.quiz import Question, QuizResult
from models import db
from config import Config

quiz = Blueprint('quiz', __name__)

@quiz.route('/quiz')
@login_required
def take_quiz():
    questions = Question.query.order_by(db.func.random()).limit(Config.QUESTIONS_PER_QUIZ).all()
    return render_template('quiz/quiz.html', questions=questions)

@quiz.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    score = 0
    questions = Question.query.all()
    
    for question in questions:
        answer = request.form.get(f'question_{question.id}')
        if answer and question.check_answer(answer):
            score += Config.POINTS_PER_QUESTION

    quiz_result = QuizResult(user_id=current_user.id, score=score)
    db.session.add(quiz_result)
    
    current_user.update_highest_score(score)
    db.session.commit()
    
    flash(f'Sınavı tamamladınız! Puanınız: {score}', 'success')
    return redirect(url_for('quiz.results'))

@quiz.route('/results')
@login_required
def results():
    user_results = QuizResult.query.filter_by(user_id=current_user.id)\
        .order_by(QuizResult.completed_at.desc()).all()
    return render_template('quiz/results.html', results=user_results)
