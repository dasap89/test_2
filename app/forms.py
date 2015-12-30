from flask.ext.wtf import Form
from wtforms import TextField, FileField
from wtforms.validators import DataRequired, Length
from app.models import Note


class NoteForm(Form):
    new_note = TextField('note',
                         validators=[DataRequired(), Length(min=10, max=255)]
                         )
    image = FileField('note image')
