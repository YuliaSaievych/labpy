import datetime
import os

from flask import render_template, request, jsonify, current_app, url_for, flash, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import login_manager, db
from app.models import User
from app.user import user_bp
from app.user.form import ChangePasswordForm, UpdateAccountForm


@user_bp.route('/users')
@login_required
def users():
    all_users = User.query.all()
    user_count = len(all_users)
    return render_template('users.html', all_users=all_users, user_count=user_count, is_authenticated=current_user.is_authenticated)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user_bp.route('/account', methods=['GET', 'POST'])
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


@user_bp.route('/change_data', methods=['GET', 'POST'])
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
        return redirect(url_for('user.account'))

    elif password_form.validate_on_submit():
        current_user.set_password(password_form.new_password.data)
        current_user.last_seen = datetime.datetime.now()
        db.session.commit()

        print("Updated user password")

        flash('Your password is changed!', 'success')
        return redirect(url_for('user.account'))

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

