import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '<KEY>'

class Config:
    SQLALCHEMY_DATABASE_URI = 'instance' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

UPLOAD_FOLDER = 'sqlite:///db.sqlite'

