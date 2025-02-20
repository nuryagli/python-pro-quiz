# Python Pro Quiz Uygulaması

Python programlama becerilerini test etmek için tasarlanmış interaktif bir web uygulaması. Discord.py, Flask, TensorFlow, OpenCV ve NLTK gibi popüler Python teknolojileri hakkında sorular içerir.

## Özellikler

- Kullanıcı kayıt ve giriş sistemi
- 5 farklı Python teknolojisi hakkında sorular
- Anlık puan hesaplama
- En yüksek puan takibi
- Responsive tasarım
- Bootstrap 5 arayüzü

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/nuryagli/python-pro-quiz.git
cd python-pro-quiz
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı başlatın:
```bash
python app.py
```

5. Tarayıcınızda şu adresi açın: `http://127.0.0.1:5000`

## Gereksinimler

- Python 3.8+
- Flask 2.3.3
- Flask-SQLAlchemy 2.5.1
- Flask-Login 0.6.3
- Flask-WTF 1.2.1
- Werkzeug 2.3.8
- Python-dotenv 1.0.0

## Proje Yapısı

```
quiz_app/
├── app.py              # Ana uygulama dosyası
├── requirements.txt    # Gerekli Python paketleri
├── README.md          # Bu dosya
└── templates/         # HTML şablonları
    ├── base.html
    ├── index.html
    ├── quiz.html
    ├── results.html
    └── auth/
        ├── login.html
        └── register.html
```

## Kullanım

1. Kayıt ol sayfasından yeni bir hesap oluşturun
2. Giriş yapın
3. Ana sayfadan "Quiz'e Başla" butonuna tıklayın
4. Soruları cevaplayın
5. Sonuçlarınızı görün ve isterseniz quiz'i tekrar çözün

## Geliştirici

- **Nurbeniz Yağlı**
- **Yıl:** 2025

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.
