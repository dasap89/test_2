from app import app, db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return '<Note %r>' % (self.notes)
