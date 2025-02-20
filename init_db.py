from app import app, db, Question, User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()

        # Admin kullanıcısını oluştur
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin kullanıcısı oluşturuldu!")

        # Örnek soruları ekle
        questions = [
            {
                'question_text': 'Discord.py botunda bir komut oluşturmak için hangi decorator kullanılır?',
                'choices': ['@commands.command()', '@bot.command()', '@discord.command()', '@client.command()'],
                'correct_answer': '@commands.command()',
                'category': 'Discord.py',
                'difficulty': 'medium',
                'points': 20
            },
            {
                'question_text': 'Flask uygulamasında route tanımlamak için hangi decorator kullanılır?',
                'choices': ['@app.route()', '@flask.route()', '@web.route()', '@route()'],
                'correct_answer': '@app.route()',
                'category': 'Flask',
                'difficulty': 'easy',
                'points': 10
            },
            {
                'question_text': 'TensorFlow\'da bir sinir ağı katmanı oluşturmak için hangi modül kullanılır?',
                'choices': ['tf.layer', 'tf.keras.layers', 'tensorflow.nn', 'tf.neural'],
                'correct_answer': 'tf.keras.layers',
                'category': 'TensorFlow',
                'difficulty': 'hard',
                'points': 30
            },
            {
                'question_text': 'OpenCV ile bir görüntüyü gri tonlamaya çevirmek için hangi fonksiyon kullanılır?',
                'choices': ['cv2.grayscale()', 'cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)', 'cv2.toGray()', 'cv2.convertGray()'],
                'correct_answer': 'cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)',
                'category': 'OpenCV',
                'difficulty': 'medium',
                'points': 20
            },
            {
                'question_text': 'NLTK kütüphanesinde tokenization işlemi için hangi fonksiyon kullanılır?',
                'choices': ['nltk.tokenize.word_tokenize()', 'nltk.word_tokenize()', 'nltk.tokenizer()', 'nltk.split_words()'],
                'correct_answer': 'nltk.tokenize.word_tokenize()',
                'category': 'NLTK',
                'difficulty': 'medium',
                'points': 20
            }
        ]

        # Veritabanında soru yoksa ekle
        if not Question.query.first():
            for q in questions:
                question = Question(
                    question_text=q['question_text'],
                    choices=q['choices'],
                    correct_answer=q['correct_answer'],
                    category=q['category'],
                    difficulty=q['difficulty'],
                    points=q['points']
                )
                db.session.add(question)
            
            db.session.commit()
            print("Sorular başarıyla eklendi!")

if __name__ == '__main__':
    init_db()
