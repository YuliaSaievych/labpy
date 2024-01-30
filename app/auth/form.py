from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[
        DataRequired(),
        Regexp('^[a-zA-Z0-9_-]{3,20}$',
               message='Username must be 3-20 characters long and can only contain letters, numbers, underscores, and hyphens'),
        Regexp('^[^_].*[^_-]$',
               message='Username cannot start or end with underscores or hyphens')
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user is None or not user.check_password(self.password.data):
            self.username.errors.append('Incorrect password or login!')
            self.password.errors.append('Incorrect password or login!')
            return False

        return True

    def validate_on_submit(self):
        return self.is_submitted() and self.validate()

