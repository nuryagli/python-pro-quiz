from datetime import datetime
from .. import db

class Question(db.Model):
    """Question model for storing quiz questions."""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'discord', 'flask', 'ai', etc.
    question = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c', or 'd'
    explanation = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question[:30]}...>'

class QuizResult(db.Model):
    """Model for storing quiz results."""
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    @property
    def percentage_score(self):
        """Calculate percentage score."""
        return round((self.score / self.total_questions) * 100)
    
    def __repr__(self):
        return f'<QuizResult {self.user_id}: {self.score}/{self.total_questions}>'
