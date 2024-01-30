from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import UPLOAD_FOLDER

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# def create_app():
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'asdasd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DEBUG'] = True

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

bcrypt.init_app(app)
db.init_app(app)
login_manager.init_app(app)

from .api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')
from .todo_bp import todo_bp
app.register_blueprint(todo_bp)

from .auth import auth_bp
app.register_blueprint(auth_bp)
from .general import general_bp
app.register_blueprint(general_bp)
from .user import user_bp
app.register_blueprint(user_bp)