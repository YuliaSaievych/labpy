from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import UPLOAD_FOLDER

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'asdasd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
