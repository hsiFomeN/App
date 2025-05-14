from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired


class ThesesForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    thesis = FileField("Содержание",
                       validators=[FileRequired(), FileAllowed(['docx', 'odt', 'txt'])])
    submit = SubmitField('Отправить')
