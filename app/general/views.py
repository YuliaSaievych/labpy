import datetime
import os

from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_required

from app.general import general_bp


my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL']


@general_bp.route('/')
def home():
    return render_template('base.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
        )


@general_bp.route('/page1')
@login_required
def page1():
    return render_account_template('page1.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
    )

@general_bp.route('/page2')
@login_required
def page2():
    return render_account_template('page2.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
    )

@general_bp.route('/page3')
@login_required
def page3():
    return render_account_template('page3.html',
        os_info=os.name,
        user_agent="Sample User Agent",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_authenticated=current_user.is_authenticated
    )

@general_bp.route('/skills')
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

def render_account_template(template_name, **kwargs):
    if request.referrer and 'account' in request.referrer:
        return render_template(template_name, **kwargs)
    else:
        return redirect(url_for('user.account'))