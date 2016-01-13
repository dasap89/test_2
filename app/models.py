import datetime
from app import app, db
from wtforms import FileField


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(255), unique=True)
    image_path = db.Column(db.String(255))

    def __repr__(self):
        return '<Note %r %r>' % (self.notes, self.image_path)


class RequestToApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_time = db.Column(db.DateTime)
    method = db.Column(db.String(5))
    path_info = db.Column(db.String(200))
    server_protocol = db.Column(db.String(10))
    server_address = db.Column(db.String(50))
    server_port = db.Column(db.String(5))
    viewed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Request to %r at %r>' % (self.path_info, self.request_time)
