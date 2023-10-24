from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import REGEX_PATTERN


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 512)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Regexp(REGEX_PATTERN),
                    Optional()]
    )
    submit = SubmitField('Создать')
