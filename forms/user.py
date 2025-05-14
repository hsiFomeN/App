from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, TelField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    phone_number = TelField('Рабочий телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    name = StringField('Имя участника', validators=[DataRequired()])
    surname = StringField('Фамилия участника', validators=[DataRequired()])
    middle_name = StringField('Отчество участника', validators=[DataRequired()])

    academic_degree = StringField("Учёная степень", validators=[DataRequired()])
    position = StringField("Должность", validators=[DataRequired()])
    academic_title = StringField("Учёное звание", validators=[DataRequired()])
    organisation = StringField("Организация", validators=[DataRequired()])
    address = StringField('Город', validators=[DataRequired()])

    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')