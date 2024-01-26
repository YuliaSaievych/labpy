from flask_bcrypt import Bcrypt
from flask_login import UserMixin

from app import db, app

bcrypt = Bcrypt(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(500))
    done = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(25), default="IN_PROGRESS")

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), unique=False, nullable=False, default='./app/static/images/image1')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', image_file='{self.image_file}')"


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    teacher = db.Column(db.String(100))

