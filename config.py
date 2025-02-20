import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///quiz.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uygulama sabitleri
    QUESTIONS_PER_QUIZ = 5
    POINTS_PER_QUESTION = 20
    
    #Login ayarları
    LOGIN_VIEW = 'auth.login'
    LOGIN_MESSAGE = 'Bu sayfayi goruntulemek icin giris yapmalisiniz.'
    LOGIN_MESSAGE_CATEGORY = 'info'
