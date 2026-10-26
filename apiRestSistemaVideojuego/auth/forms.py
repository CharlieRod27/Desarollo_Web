from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from models import User

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")

class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(3, 64)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Confirmar contraseña", validators=[
        DataRequired(), EqualTo("password", message="Las contraseñas no coinciden")])
    submit = SubmitField("Registrarme")

    def validate_username(self, field):   # WTForms ejecuta automáticamente validate_<campo>
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ese usuario ya existe.")