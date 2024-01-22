import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '<KEY>'

UPLOAD_FOLDER = 'sqlite:///db.sqlite'

SQLALCHEMY_DATABASE_URI = 'instance' + os.path.join(basedir, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False