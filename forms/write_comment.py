from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    comment = TextAreaField('Оставьте отзыв', validators=[DataRequired()])
    submit = SubmitField('Отправить')
