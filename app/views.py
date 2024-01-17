from flask import Flask, render_template, url_for, redirect, request, session, flash
import os
import datetime
import json
from flask import jsonify

from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash


from app import app, db
from app.form import ToDoForm
from app.models import ToDo

app.config['SECRET_KEY'] = 'asdasd'

# List of skills
my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL']

with open("app/static/js/users.json", "r") as file:
    users = json.load(file)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id



@login_manager.user_loader
def user_loader(username):
    user = next((u for u in users if u['username'] == username), None)
    if user is None:
        return None

    user_obj = User(id=user['username'])
    return user_obj


class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = next((u for u in users if u['username'] == self.username.data), None)

        if user is None or user['password'] != self.password.data:
            self.username.errors.append('Incorrect password or login!')
            self.password.errors.append('Incorrect password or login!')
            return False

        return True

    def validate_on_submit(self):
        if self.is_submitted() and self.validate():
            user = User(id=self.username.data)
            login_user(user, remember=self.remember.data)
            flash('Login successful', 'success')
            return True
        return False

@app.route('/')
def home():
    os_info = os.name
    user_agent = "Sample User Agent"  # You may use request.user_agent to get the actual user agent
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('base.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


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
        # Display all skills and their total count
        skills_count = len(my_skills)
        return render_template('page_skills.html', skills=my_skills, skills_count=skills_count)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', form=form, title="Register")



@app.route('/login', methods=['GET', 'POST'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = LoginForm()
    if form.validate_on_submit():
        login_user(current_user, remember=form.remember.data)
        flash('Login successful', 'success')
        return redirect(url_for('info'))
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
    user_data = session.get('user_data', current_user.id)

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