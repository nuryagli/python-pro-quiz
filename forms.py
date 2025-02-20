from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app import User

class LoginForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired()])
    password = PasswordField('Sıfre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatirla')
    submit = SubmitField('Giris Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    password = PasswordField('Sifre', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Sifre Tekrar', validators=[
        DataRequired(),
        EqualTo('password', message='Sifreler eslesmiyor!')
    ])
    submit = SubmitField('Kayit Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanici adi zaten kullaniliyor!')
