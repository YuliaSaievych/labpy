from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, Email, Regexp, EqualTo
from wtforms.fields.simple import PasswordField, StringField, BooleanField

from app.models import User


class ToDoForm(FlaskForm):
    title = StringField("", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField("Save")

class UpdateTodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(message="This field is required.")])
    status = StringField("Status", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField('Update')


class UpdateAccountForm(FlaskForm):
    username = StringField('Ім\'я', validators=[
        DataRequired(),
        Length(min=4, max=14, message="This required field must be between 4 and 14 characters long"),
        Regexp(r'^[A-Za-z .]+$', message='The username can contain only Latin letters, spaces and periods.')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="This is a required field")])
    profile_picture = FileField('Profile picture', validators=[
        FileAllowed(['jpg', 'png'], 'Only files with the extension .jpg або .png.')
    ])
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please select another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use. Please select another one.')

    submit = SubmitField('Update your profile')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[Length(min=6, message="Password must be more than 6 characters")])
    confirm_new_password = PasswordField('Repeat your new password', validators=[EqualTo('new_password', message='Passwords must be the same')])
    submit_change_password = SubmitField('Change Password')

class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[
        DataRequired(),
        Regexp('^[a-zA-Z0-9_-]{3,20}$',
               message='Username must be 3-20 characters long and can only contain letters, numbers, underscores, and hyphens'),
        Regexp('^[^_].*[^_-]$',  # Additional regular expression
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

