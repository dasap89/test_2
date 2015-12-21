import datetime
from app import app, db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return '<Note %r>' % (self.notes)


class Request_to_App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_time = db.Column(db.DateTime, default=datetime.datetime.now())
    method = db.Column(db.String(5))
    path_info = db.Column(db.String(200))
    server_protocol = db.Column(db.String(10))
    server_address = db.Column(db.String(50))
    server_port = db.Column(db.String(5))
