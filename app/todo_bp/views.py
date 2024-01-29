import platform

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required

from app import db
from . import todo_bp
from .forms import ToDoForm
from app.models import ToDo
from app.todo_bp.forms import UpdateTodoForm


@todo_bp.route('/todo', methods=["GET"])
@login_required
def todo_page():
    def base_render(template: str, **context):
        return render_template(template, about_os=platform.platform(), user_agent_info=request.user_agent.string, **context)

    return base_render("ToDo.html", todo_list=ToDo.query.all(), todo_form=ToDoForm(), update_form=UpdateTodoForm())

@todo_bp.route("/todo", methods=["POST"])
@login_required
def add_todo():
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        new_todo = ToDo(title=todo_form.title.data, done=False, status='IN_PROGRESS')
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully', 'success')
    return redirect(url_for("todo.todo_page"))

@todo_bp.route("/todo/<string:id>/update", methods=["GET", "POST"])
@login_required
def update_todo(id: str):
    todo = db.get_or_404(ToDo, id)

    update_form = UpdateTodoForm()

    if update_form.validate_on_submit():
        todo.title = update_form.title.data
        todo.status = update_form.status.data
        db.session.commit()
        flash('Todo updated successfully', 'success')
        return redirect(url_for("todo.todo_page"))

    return render_template("update_todo.html", todo=todo, update_form=update_form)



@todo_bp.route("/todo/<string:id>/delete", methods=["GET"])
@login_required
def delete_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')

    return redirect(url_for("todo.todo_page"))