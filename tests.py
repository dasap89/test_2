#!flask/bin/python
import os
import unittest
import io

from app import app, db
from config import basedir

from app.models import Note
from flask import url_for
from flask import render_template
from app.models import Note, RequestToApp
from app.views import list_notes


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
        client = app.test_client()
        with app.test_request_context('/'):
            response = client.get(url_for('list_notes'))
        assert response.status_code == 200, u'Status code is not 200'
        assert response.data is not None, u'There is no data in response'

    def test_safe_note(self):
        note = Note(notes="Some note #1")
        db.session.add(note)
        db.session.commit()
        check_note = Note.query.first()
        assert check_note == note, u'Test note not saved in database'

    def test_add_note(self):
        client = app.test_client()
        with app.test_request_context('/'):
             post = client.post(url_for('list_notes'), data={'new_note': 'Some note #1'})
        self.assertEqual(post.status_code, 200)
        self.assertTrue('Some note #1' in post.data)

    def test_show_note(self):
        note = Note(notes="Some note #1")
        db.session.add(note)
        db.session.commit()
        client = app.test_client()
        with app.test_request_context('/'):
            response = client.get(url_for('list_notes'))
        assert response.status_code == 200, u'Status code is not 200'
        assert note.notes in response.data, u'There is no test entry'

    def test_html_widget(self):
        client = app.test_client()
        with app.test_request_context('/'):
            response = client.get(url_for('add_note'))
        assert response.status_code == 200, u'Status code is not 200'
        assert '<script type="text/javascript" src=' in response.data
        with app.test_request_context('/'):
            response = client.get(url_for('widget'))
        self.assertEqual(response.status_code, 200)
        assert len(response.data) >= 0, u'Widget page is empty'

    def test_ajax_form(self):
        client = app.test_client()
        with app.test_request_context('/'):
            response1 = client.get(url_for('list_notes'))
        assert 'No notes in database' in response1.data
        with app.test_request_context('/'):
            response2 = client.get(url_for('ajax_form'))
        assert response2.status_code is 200
        with app.test_request_context('/'):
            post = client.post(url_for('ajax_add'), data={'note': 'Some note #1'})  # noqa
        self.assertEqual(post.status_code, 200)
        with app.test_request_context('/'):
            response3 = client.get(url_for('list_notes'))
        assert 'Some note #1' in response3.data

    def test_add_note_with_image(self):
        client = app.test_client()
        with app.test_request_context('/'):
            response1 = client.get(url_for('list_notes'))
        assert 'No notes in database' in response1.data
        with app.test_request_context('/'):
            post = client.post(url_for('add_note'), data=dict(new_note='Some note #1', image=(io.BytesIO(b'this is a test'), 'test.jpeg')), follow_redirects=True)  # noqa
        # post = self.app.post('/add-note/', data=dict(new_note='Some note #1', image=(io.BytesIO(b'this is a test'), 'test.jpeg')), follow_redirects=True)  # noqa
        self.assertEqual(post.status_code, 200)
        with app.test_request_context('/'):
            response = client.get(url_for('list_notes'))
        
        self.assertTrue('Some note #1' in response.data)
        self.assertTrue('<img src="/static/uploads/test.jpeg"/>' in response.data)  # noqa

    def test_middleware_save_requests(self):
        client = app.test_client()
        with app.test_request_context('/'):
            response = client.get(url_for('request_to_app'))
        self.assertEqual(response.status_code, 200)
        with app.test_request_context('/'):
            response = client.get(url_for('table'))
        self.assertEqual(response.status_code, 200)

    def test_requests_page_return_only_10_records(self):
        client = app.test_client()
        for i in range(0, 20):
            with app.test_request_context('/'):
                response = client.get(url_for('request_to_app'))
            self.assertEqual(response.status_code, 200)
        with app.test_request_context('/'):
            response = client.get(url_for('table'))
        self.assertEqual(response.status_code, 200)
        count = response.data.count('/requests', 0, len(response.data))
        self.assertEqual(count, 10)

    def test_middleware_doesnt_save_ajax_requests(self):
        client = app.test_client()
        with app.test_request_context('/'):
                response = client.get(
                    url_for('request_to_app'),
                    headers=[('X-Requested-With', 'XMLHttpRequest')]
                )
        requsts_stored_in_db = len(RequestToApp.query.all())
        self.assertEquals(requsts_stored_in_db, 0)


if __name__ == '__main__':
    unittest.main()
