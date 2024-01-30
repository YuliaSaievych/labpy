
from flask import request

from app import db
from app.models import ToDo
from . import todo_api_bp


@todo_api_bp.route("/", methods=["POST"])
def add():
    data = request.json
    todo = ToDo(title=data['title'], description=data['description'], done=data['done'], status=data['status'])
    db.session.add(todo)
    db.session.commit()

    return to_json(todo), 201


@todo_api_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.json
    todo = ToDo.query.get_or_404(id)
    todo.title = data['title']
    todo.description = data['description']
    todo.done = data['done']
    todo.status = data['status']

    db.session.commit()
    return to_json(todo), 200


def to_json(todo: ToDo):
    return {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'done': todo.done,
        'status': todo.status
    }


@todo_api_bp.route("/<int:id>", methods=["GET"])
def get(id):
    todo = ToDo.query.get_or_404(id)
    return to_json(todo)


@todo_api_bp.route("/all", methods=["GET"])
def get_all():
    return [to_json(todo) for todo in ToDo.query.all()]


@todo_api_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    todo = ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return {'status': 'Deleted'}, 200
