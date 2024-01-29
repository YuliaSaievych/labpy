from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import UPLOAD_FOLDER

db = SQLAlchemy()
bcrypt = Bcrypt()

# def create_app():
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'asdasd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

bcrypt.init_app(app)
db.init_app(app)

from . import views
from .api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')
from .todo_bp import todo_bp
app.register_blueprint(todo_bp)
