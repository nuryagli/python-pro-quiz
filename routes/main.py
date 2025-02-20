from flask import Blueprint, render_template
from flask_login import current_user
from models.quiz import QuizResult

main = Blueprint('main', __name__)

@main.route('/')
def index():
    highest_score = QuizResult.query.with_entities(QuizResult.score).order_by(QuizResult.score.desc()).first()
    highest_score = highest_score[0] if highest_score else 0
    
    user_highest = 0
    if current_user.is_authenticated:
        user_highest = current_user.highest_score
        
    return render_template('index.html', 
                         highest_score=highest_score, 
                         user_highest=user_highest)
