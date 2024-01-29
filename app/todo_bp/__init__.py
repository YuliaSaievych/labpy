from flask import Blueprint

todo_bp = Blueprint("todo_api", __name__)

from . import views