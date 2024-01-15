from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    title = StringField("", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField("Save")