import os
from app import app


@app.route('/list-notes')
def list_notes():
    return 'Hello World'