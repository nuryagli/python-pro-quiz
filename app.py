from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    confirm_password = PasswordField('Şifre Tekrar', validators=[DataRequired()])
    submit = SubmitField('Kayıt Ol')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_scores():
    highest_score = db.session.query(db.func.max(User.highest_score)).scalar() or 0
    user_highest = current_user.highest_score if current_user.is_authenticated else 0
    return dict(highest_score=highest_score, user_highest=user_highest)


# Quiz soruları
questions = [
    {
        'id': 1,
        'question': 'Discord.py botunda bir komut oluşturmak için hangi decorator kullanılır?',
        'choices': ['@commands.command()', '@bot.command()', '@discord.command()', '@client.command()'],
        'correct_answer': '@commands.command()'
    },
    {
        'id': 2,
        'question': 'Flask uygulamasında route tanımlamak için hangi decorator kullanılır?',
        'choices': ['@app.route()', '@flask.route()', '@web.route()', '@route()'],
        'correct_answer': '@app.route()'
    },
    {
        'id': 3,
        'question': 'TensorFlow\'da bir sinir ağı katmanı oluşturmak için hangi modül kullanılır?',
        'choices': ['tf.layer', 'tf.keras.layers', 'tensorflow.nn', 'tf.neural'],
        'correct_answer': 'tf.keras.layers'
    },
    {
        'id': 4,
        'question': 'OpenCV ile bir görüntüyü gri tonlamaya çevirmek için hangi fonksiyon kullanılır?',
        'choices': ['cv2.grayscale()', 'cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)', 'cv2.toGray()', 'cv2.convertGray()'],
        'correct_answer': 'cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'
    },
    {
        'id': 5,
        'question': 'NLTK kütüphanesinde tokenization işlemi için hangi fonksiyon kullanılır?',
        'choices': ['nltk.tokenize.word_tokenize()', 'nltk.word_tokenize()', 'nltk.tokenizer()', 'nltk.split_words()'],
        'correct_answer': 'nltk.tokenize.word_tokenize()'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.form.get(f"question_{question['id']}")
            if user_answer and user_answer == question['correct_answer']:
                score += 20

        # Kullanıcının son skorunu güncelle
        current_user.last_score = score
        if score > current_user.highest_score:
            current_user.highest_score = score

        # Yeni quiz sonucunu kaydet
        quiz_result = QuizResult(user_id=current_user.id, score=score)
        db.session.add(quiz_result)
        db.session.commit()

        flash(f'Quiz tamamlandı! Puanınız: {score}')
        return redirect(url_for('results'))

    return render_template('quiz.html', questions=questions)

@app.route('/results')
@login_required
def results():
    return render_template('results.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Geçersiz kullanıcı adı veya şifre')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Bu kullanıcı adı zaten kullanılıyor')
            return redirect(url_for('register'))
        
        if form.password.data != form.confirm_password.data:
            flash('Şifreler eşleşmiyor')
            return redirect(url_for('register'))
            
        user = User(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
