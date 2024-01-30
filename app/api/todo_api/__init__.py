from flask import Blueprint

todo_api_bp = Blueprint("todo_api", __name__)

from . import views