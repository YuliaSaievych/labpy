from app import db

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(500))
    done = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(25), default="IN_PROGRESS")
