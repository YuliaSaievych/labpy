import datetime
import os

from flask import redirect, flash, url_for, render_template, request, session
from flask_login import current_user, login_user, login_required, logout_user

from app import db
from app.models import User
from . import auth_bp
from .form import RegisterForm, LoginForm


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=form.username.data, email=form.email.data, image_file='')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for("auth.login"))
    return render_template('register.html',
        form=form,
        title="Register",
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data, force=True)
            db.session.add(user)
            db.session.commit()
            flash('Login successful', 'success')
            return redirect(url_for('user.account'))
        else:
            flash('Incorrect password or login!', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html',
        form=form,
        data=data,
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


@auth_bp.route('/logout')
@login_required
def logout():
    user_data = session.pop('user_data', current_user.id)
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('auth.login', user_data=user_data))

