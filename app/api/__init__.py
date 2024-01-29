from flask import Blueprint

api_bp = Blueprint("api", __name__)

from .todo_api import todo_api_bp
api_bp.register_blueprint(todo_api_bp, url_prefix='/api')