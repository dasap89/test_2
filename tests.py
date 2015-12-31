#!flask/bin/python
import os
import unittest

from app import app, db
from config import basedir
from app.models import Note, Request_to_App


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
        assert response.status_code == 200, u'Status code is not 200'
        assert response.data is not None, u'There is no data in response'

    def test_middleware_save_requests(self):
        response = self.app.get('/requests')
        self.assertEqual(response.status_code, 301)
        response = self.app.get('/requests/table/')
        print response
        self.assertEqual(response.status_code, 200)
        print response.data
        # self.assertEqual(len(response.context['new_requests']), 10)
    
    
    def test_requests_page_return_10_records(self):
        for i in range(0, 20):
            response = self.app.get('/requests')
            print response.data
            self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['new_requests']), 10)

    '''def test_if_requests_view_returns_valid_data(self):
        response = self.app.get('/requests')
        print response
        self.assertEqual(response.status_code, 200)
        content = response.context['new_requests'][0]
        data = Requests.objects.first()
        self.assertEqual(content, data)'''

    def test_middleware_doesnt_save_ajax_requests(self):
        self.app.get('/requests',
                        headers=[('X-Requested-With', 'XMLHttpRequest')])
        requsts_stored_in_db = len(Request_to_App.query.all())
        self.assertEquals(requsts_stored_in_db, 0)

if __name__ == '__main__':
    unittest.main()
