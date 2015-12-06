#!flask/bin/python
import os
import unittest

from app import app, db
from config import basedir
from app.models import Note


class TestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page(self):
        all_notes = Note.query.all()
        assert len(all_notes) > 0, u'The database has no entries'
        response = self.app.get('/list-notes')
        assert response.status_code == 200, u'Status code is %s' % response.status_code
        assert response.data is not None, u'There is no data in response'

if __name__ == '__main__':
    unittest.main()