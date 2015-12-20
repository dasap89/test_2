#!flask/bin/python
import os
import unittest

from app import app, db
from config import basedir
from app.models import Note
from flask import url_for


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')  # noqa
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page(self):
        note1 = Note(notes="First Note")
        note2 = Note(notes="Second Note")
        db.session.add(note1)
        db.session.add(note2)
        db.session.commit()
        all_notes = Note.query.all()
        assert len(all_notes) > 0, u'The database has no entries'
        response = self.app.get('/list-notes/')
        assert response.status_code == 200, u'Status code is %s' % response.status_code  # noqa
        assert response.data is not None, u'There is no data in response'

    def test_safe_note(self):
        note = Note(notes="Some note #1")
        db.session.add(note)
        db.session.commit()
        check_note = Note.query.first()
        assert check_note == note, u'Test note not saved in database'

    def test_add_note(self):
        post = self.app.post('/list-notes/', data={'new_note': 'Some note #1'})
        self.assertEqual(post.status_code, 200)
        self.assertTrue('Some note #1' in post.data)

    def test_show_note(self):
        note = Note(notes="Some note #1")
        db.session.add(note)
        db.session.commit()
        response = self.app.get('/list-notes/')
        assert response.status_code == 200, u'Status code is not 200'
        assert note.notes in response.data, u'There is no test entry'

if __name__ == '__main__':
    unittest.main()
