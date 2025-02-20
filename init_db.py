from app import create_app, db
from app.models import User, Question

def init_db():
    app = create_app()
    with app.app_context():
        # veritabaniuni olusturuyoruz.
        db.create_all()

        # Mevcut tum sorulari sil
        Question.query.delete()
        
        # ornek kullanici
        if not User.query.filter_by(username="demo").first():
            demo_user = User(username="demo")
            demo_user.password = "demo123"  
            db.session.add(demo_user)

        # sorular
        questions = [
            {
                "question": "Discord.py'da bir sunucunun tum rollerini almak icin hangi ozellik kullanilir?",
                "option_a": "server.roles",
                "option_b": "guild.roles",
                "option_c": "discord.roles",
                "option_d": "client.roles",
                "correct_answer": "b",
                "category": "Discord.py"
            },
            {
                "question": "Flask uygulamasinda kullanicinin yukledigi dosyalari guvenli bir sekilde kaydetmek icin hangi fonksiyon kullanilir?",
                "option_a": "file.save()",
                "option_b": "secure_filename()",
                "option_c": "save_file()",
                "option_d": "upload_file()",
                "correct_answer": "b",
                "category": "Flask"
            },
            {
                "question": "TensorFlow'da bir CNN modelinde max pooling katmaninin amaci nedir?",
                "option_a": "Aktivasyon fonksiyonu eklemek",
                "option_b": "Overfitting'i onlemek",
                "option_c": "Boyut azaltma ve onemli ozellikleri koruma",
                "option_d": "Gradient vanishing problemini cozme",
                "correct_answer": "c",
                "category": "AI"
            },
            {
                "question": "BeautifulSoup'ta belirli bir CSS sinifina sahip tum elementleri secmek icin hangi metod kullanilir?",
                "option_a": "find_class()",
                "option_b": "select('.class_name')",
                "option_c": "get_elements_by_class()",
                "option_d": "find_all(class='class_name')",
                "correct_answer": "d",
                "category": "Web Scraping"
            },
            {
                "question": "NLTK'da bir metnin duygusal analizi (sentiment analysis) icin hangi siniflandirici en sik kullanilir?",
                "option_a": "NaiveBayesClassifier",
                "option_b": "SentimentClassifier",
                "option_c": "TextClassifier",
                "option_d": "EmotionAnalyzer",
                "correct_answer": "a",
                "category": "NLP"
            },
            {
                "question": "ImageAI ile egitilmis bir nesne algilama modelini yuklerken hangi parametre modelin hizini belirler?",
                "option_a": "detection_speed",
                "option_b": "model_speed",
                "option_c": "inference_speed",
                "option_d": "processing_speed",
                "correct_answer": "a",
                "category": "Computer Vision"
            },
            {
                "question": "Discord.py'da bir mesaja tepki (reaction) eklemek icin hangi coroutine kullanilir?",
                "option_a": "message.react()",
                "option_b": "message.add_reaction()",
                "option_c": "message.create_reaction()",
                "option_d": "message.send_reaction()",
                "correct_answer": "b",
                "category": "Discord.py"
            },
            {
                "question": "Flask-SQLAlchemy'de bir sorguyu belirli bir sutuna gore azalan sirada siralamak icin hangi metod kullanilir?",
                "option_a": "sort_by()",
                "option_b": "order_by()",
                "option_c": "desc()",
                "option_d": "sort_desc()",
                "correct_answer": "b",
                "category": "Flask"
            },
            {
                "question": "TensorFlow'da transfer learning yaparken hangi katmanlar genellikle dondurulur (freeze)?",
                "option_a": "Sadece cikis katmani",
                "option_b": "Sadece giris katmani",
                "option_c": "Ilk convolutional katmanlar",
                "option_d": "Son fully connected katmanlar",
                "correct_answer": "c",
                "category": "AI"
            },
            {
                "question": "NLTK'da bir kelimenin konusma parcasi (part of speech) etiketini bulmak icin hangi fonksiyon kullanilir?",
                "option_a": "word_tag()",
                "option_b": "pos_tag()",
                "option_c": "speech_tag()",
                "option_d": "get_pos()",
                "correct_answer": "b",
                "category": "NLP"
            }
        ]

        # Yeni sorular
        for q_data in questions:
            question = Question(**q_data)
            db.session.add(question)

        db.session.commit()
        print("Veritabani basariyla olusturuldu ve ornek veriler eklendi!")

if __name__ == "__main__":
    init_db()
