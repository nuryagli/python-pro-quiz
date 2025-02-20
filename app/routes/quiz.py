from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import Question, QuizResult, User
from .. import db
from sqlalchemy import func
import random

bp = Blueprint('quiz', __name__)

@bp.route('/quiz')
@login_required
def start_quiz():
    # Get 5 random questions
    questions = Question.query.order_by(func.random()).limit(5).all()
    
    # Get highest scores
    highest_overall = db.session.query(func.max(User.highest_score)).scalar() or 0
    
    return render_template('quiz/quiz.html', 
                         questions=questions,
                         highest_score=highest_overall)

@bp.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    answers = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = int(key.split('_')[1])
            answers[question_id] = value
    
    questions = Question.query.filter(Question.id.in_(answers.keys())).all()
    correct_answers = 0
    total_questions = len(questions)
    
    for question in questions:
        if answers.get(question.id) == question.correct_answer:
            correct_answers += 1
    
    percentage_score = round((correct_answers / total_questions) * 100)
    
    # Save quiz result
    quiz_result = QuizResult(
        user_id=current_user.id,
        score=correct_answers,
        total_questions=total_questions
    )
    db.session.add(quiz_result)
    
    # Update user's highest score if necessary
    current_user.update_highest_score(percentage_score)
    db.session.commit()
    
    flash(f'Quiz tamamlandı! Puanınız: {percentage_score}%', 'success')
    return redirect(url_for('quiz.results'))

@bp.route('/results')
@login_required
def results():
    # Get user's quiz history
    user_results = QuizResult.query.filter_by(user_id=current_user.id)\
        .order_by(QuizResult.date.desc()).limit(10).all()
    
    # Get highest scores
    highest_overall = db.session.query(func.max(User.highest_score)).scalar() or 0
    
    return render_template('quiz/results.html',
                         results=user_results,
                         highest_score=highest_overall)
