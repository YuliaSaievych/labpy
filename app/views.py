import datetime
import os

from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Regexp

from app import db
from app.form import ToDoForm
from app.models import ToDo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdasd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL']

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


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
            # user = User.query.filter_by(username=self.username.data).first()
            # if user is None:
            #     new_user = User(username=self.username.data, email=self.email.data)
            #     new_user.set_password(self.password.data)
            #     db.session.add(new_user)
            #     db.session.commit()
            #     login_user(new_user, remember=self.remember.data)
            #     flash('Registration successful', 'success')
            #     return True
            # else:
            #     flash('Username or email already exists. Please choose another.', 'danger')
       # return False


@app.route('/')
def home():
    os_info = os.name
    user_agent = "Sample User Agent"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('base.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    user_count = len(all_users)
    return render_template('users.html', all_users=all_users, user_count=user_count)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None

    user_obj = User(id=user.id)
    return user_obj


@app.route('/todo', methods=["GET"])
def todo_page():
    return "todo_page"


@app.route("/todo", methods=["POST"])
def add_todo():
    todo_form = ToDoForm()
    new_todo = ToDo(title=todo_form.title.data, done=False, status="IN_PROGRESS")
    db.session.add(new_todo)
    db.session.commit()

    flash('Todo added successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/todo/<string:id>")
def delete_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/todo/<string:id>/update")
def update_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    todo.done = True
    todo.status = "UPDATED"

    db.session.commit()
    flash('Todo updated successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route('/page1')
def page1():
    return render_template('page1.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/page3')
def page3():
    return render_template('page3.html')


@app.route('/skills')
@app.route('/skills/<int:id>')
def display_skills(id=None):
    if id is not None:
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return f"Skill {id + 1}: {skill}"
        else:
            return "Invalid skill ID"
    else:
        skills_count = len(my_skills)
        return render_template('page_skills.html', skills=my_skills, skills_count=skills_count)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', form=form, title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = LoginForm()

    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data, force=True)
        db.session.add(user)
        db.session.commit()
        flash('Login successful', 'success')
        return redirect(url_for('info'))
    else:
        flash('Incorrect password or login!', 'danger')
    return render_template('login.html', form=form, data=data)


@app.route('/logout')
@login_required
def logout():
    user_data = session.pop('user_data', current_user.id)
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login', user_data=user_data))


@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    user_data = current_user.id

    if request.method == 'POST':
        action = request.form.get('action')
        key = request.form.get('key')

        if action == 'add':
            value = request.form.get('value')
            expiry_days = int(request.form.get('expiry_days', 1))

            response = jsonify({'success': True, 'message': 'Cookie added successfully'})
            response.set_cookie(key, value, max_age=expiry_days * 24 * 60 * 60)
            return response

        elif action == 'delete':
            response = jsonify({'success': True, 'message': 'Cookie deleted successfully'})
            response.delete_cookie(key)
            return response

        elif action == 'delete_all':
            response = jsonify({'success': True, 'message': 'All cookies deleted successfully'})
            for cookie in request.cookies:
                response.delete_cookie(cookie)
            return response

    return render_template('info.html', data=data, user_data=user_data)
