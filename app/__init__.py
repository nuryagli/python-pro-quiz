from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import json
from sqlalchemy.types import TypeDecorator, VARCHAR
import os

class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
admin = Admin(app, name='Python Pro Quiz Admin', template_mode='bootstrap3')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    choices = db.Column(JSONEncodedDict, nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=10)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    answers = db.Column(JSONEncodedDict)

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Question, db.session))
admin.add_view(SecureModelView(QuizResult, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_scores():
    highest_score = db.session.query(db.func.max(User.highest_score)).scalar() or 0
    user_highest = current_user.highest_score if not current_user.is_anonymous else 0
    return dict(highest_score=highest_score, user_highest=user_highest)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        score = 0
        user_answers = {}
        questions = Question.query.all()
        
        for question in questions:
            user_answer = request.form.get(f"question_{question.id}")
            user_answers[str(question.id)] = user_answer
            
            if user_answer and user_answer == question.correct_answer:
                score += question.points

        # Kullanıcının son skorunu güncelle
        current_user.last_score = score
        if score > current_user.highest_score:
            current_user.highest_score = score

        # Yeni quiz sonucunu kaydet
        quiz_result = QuizResult(
            user_id=current_user.id, 
            score=score,
            answers=user_answers
        )
        db.session.add(quiz_result)
        db.session.commit()

        flash(f'Quiz tamamlandı! Puanınız: {score}')
        return redirect(url_for('results'))

    questions = Question.query.all()
    return render_template('quiz.html', questions=questions)

@app.route('/results')
@login_required
def results():
    user_results = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.date.desc()).limit(5).all()
    return render_template('results.html', results=user_results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Geçersiz kullanıcı adı veya şifre')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor')
            return redirect(url_for('register'))
        
        user = User(username=username)
        user.password_hash = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Veritabanını sil
    if os.path.exists('../../quiz.db'):
        os.remove('../../quiz.db')
    
    with app.app_context():
        # Veritabanını yeniden oluştur
        db.create_all()
        
        # Admin kullanıcısı oluştur
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            
    app.run(debug=True)
