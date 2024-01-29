from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import DataRequired


class ToDoForm(FlaskForm):
    title = StringField("", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField("Save")

class UpdateTodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(message="This field is required.")])
    status = StringField("Status", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField('Update')