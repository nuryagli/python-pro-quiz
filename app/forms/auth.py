from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from ..models import User

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Kullanıcı Adı', 
                         validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Şifre', 
                           validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifreyi Onayla', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')
    
    def validate_username(self, field):
        """Check if username is already taken."""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor.')
