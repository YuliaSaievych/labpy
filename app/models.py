from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.ext.serializer import Serializer

from app import db, bcrypt

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

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('asdasd')
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', image_file='{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String)
    image = db.Column(db.String, default='postdefault.jpg')
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    type = db.Column(db.Enum('news', 'publication', 'other'), default='other')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, type={self.type}, created={self.created}, enabled={self.enabled})>"



