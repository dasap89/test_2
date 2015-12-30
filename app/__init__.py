import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/app/static/uploads'

from app import views, models  # noqa
