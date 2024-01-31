
from flask import request
from flask_httpbasicauth import HTTPBasicAuth

from app import db
from app.models import ToDo
from . import todo_api_bp
from ...todo_bp.utils import to_json

auth = HTTPBasicAuth()

@todo_api_bp.route("/", methods=["POST"])
@auth.login_required
def add():
    data = request.json
    todo = ToDo(title=data['title'], description=data['description'], done=data['done'], status=data['status'])
    db.session.add(todo)
    db.session.commit()
    return to_json(todo), 201


@todo_api_bp.route("/<int:id>", methods=["PUT"])
@auth.login_required
def update(id):
    data = request.json
    todo = ToDo.query.get_or_404(id)
    todo.title = data['title']
    todo.description = data['description']
    todo.done = data['done']
    todo.status = data['status']
    db.session.commit()
    return to_json(todo), 200

@todo_api_bp.route("/<int:id>", methods=["GET"])
@auth.login_required
def get(id):
    todo = ToDo.query.get_or_404(id)
    return to_json(todo)

@todo_api_bp.route("/all", methods=["GET"])
@auth.login_required
def get_all():
    return [to_json(todo) for todo in ToDo.query.all()]

@todo_api_bp.route("/<int:id>", methods=["DELETE"])
@auth.login_required
def delete(id):
    todo = ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return {'status': 'Deleted'}, 200
