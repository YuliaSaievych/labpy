import datetime
import os

from app import app, db

from flask import jsonify, current_app, request, session, flash, render_template, redirect, url_for
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from werkzeug.utils import secure_filename

from app.form import UpdateAccountForm, ChangePasswordForm, RegisterForm, LoginForm
from app.models import User




my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL']

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/')
def home():
    return render_template('base.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    user_count = len(all_users)
    return render_template('users.html', all_users=all_users, user_count=user_count, is_authenticated=current_user.is_authenticated)





@app.route('/page1')
@login_required
def page1():
    return render_account_template('page1.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
    )

@app.route('/page2')
@login_required
def page2():
    return render_account_template('page2.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
    )

@app.route('/page3')
@login_required
def page3():
    return render_account_template('page3.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
    )

@app.route('/skills')
@login_required
def display_skills(id=None):
    if id is not None:
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return f"Skill {id + 1}: {skill}"
        else:
            return "Invalid skill ID"
    else:
        skills_count = len(my_skills)
        return render_account_template('page_skills.html',
            skills=my_skills,
            skills_count=skills_count,
            os_info=os.name,
            user_agent="Sample User Agent",
            current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_authenticated=current_user.is_authenticated
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=form.username.data, email=form.email.data, image_file='')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for("login"))
    return render_template('register.html',
        form=form,
        title="Register",
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


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
        return redirect(url_for('account'))
    else:
        flash('Incorrect password or login!', 'danger')
    return render_template('login.html',
        form=form,
        data=data,
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


@app.route('/logout')
@login_required
def logout():
    user_data = session.pop('user_data', current_user.id)
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login', user_data=user_data))


@app.route('/change_data', methods=['GET', 'POST'])
@login_required
def change_data():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    user_data = current_user
    account_form = UpdateAccountForm(obj=current_user)
    password_form = ChangePasswordForm()

    if account_form.validate_on_submit():
        current_user.username = account_form.username.data
        current_user.email = account_form.email.data
        current_user.last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if account_form.profile_picture.data:
            profile_picture = account_form.profile_picture.data
            filename = secure_filename(profile_picture.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(filepath)
            current_user.image_file = filename

        db.session.commit()

        print("Updated user data:")
        print(f"Username: {current_user.username}")
        print(f"Email: {current_user.email}")
        print(f"Image File: {current_user.image_file}")

        flash('Your profile is updated!', 'success')
        return redirect(url_for('account'))

    elif password_form.validate_on_submit():
        current_user.set_password(password_form.new_password.data)
        current_user.last_seen = datetime.datetime.now()
        db.session.commit()

        print("Updated user password")

        flash('Your password is changed!', 'success')
        return redirect(url_for('account'))

    return render_template('change_data.html',
                           form=account_form,
                           password_form=password_form,
                           data=data,
                           user_data=user_data,
                           os_info=os.name,
                           user_agent="Sample User Agent",
                           current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           is_authenticated=current_user.is_authenticated
                           )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    user_data = current_user

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



    return render_template('account.html',
        data=data,
        user_data=user_data,
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


def render_account_template(template_name, **kwargs):
    if request.referrer and 'account' in request.referrer:
        return render_template(template_name, **kwargs)
    else:
        return redirect(url_for('account'))