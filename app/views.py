# coding: utf-8
import os
import random
import datetime
from flask import render_template, redirect, url_for
from flask import Response, request, json, flash, make_response
from werkzeug import secure_filename

from app import app, db, ALLOWED_EXTENSIONS
from app.models import Note, RequestToApp
from app.forms import NoteForm


def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS  # noqa


@app.before_request
def before_request():
    if request.is_xhr is False and '/static/' not in request.path:
        request_to_app = RequestToApp(
            request_time=datetime.datetime.now(),
            method=request.method,
            path_info=request.path,
            server_protocol=request.environ['SERVER_PROTOCOL'],
            server_address=request.remote_addr,
            server_port=request.environ['SERVER_PORT']
            )
        db.session.add(request_to_app)
        db.session.commit()
    return None


@app.route('/list-notes/', methods=['GET', 'POST'])
def list_notes():

    form = NoteForm()
    if form.validate_on_submit():
        add_new_note = Note(notes=form.new_note.data)
        db.session.add(add_new_note)
        db.session.commit()
        flash('Your note is now live!')
        return redirect('list-notes')

    notes = Note.query.all()
    return render_template('list_notes.html', form=form, notes=notes)


@app.route('/add-note/', methods=['GET', 'POST'])
def add_note():
    form = NoteForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        note = form.new_note.data
        if request.files.get('image') is None:
            filename = None
        else:
            image = request.files['image']
            filename = ''
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_new_note = Note(notes=note, image_path=filename)
            db.session.add(add_new_note)
            db.session.commit()
            flash('Your post "%s" is now live!' % note, 'success')
            return redirect(url_for('list_notes'))
    if form.errors:
        flash(form.errors, 'danger')
    widget_link = request.url.replace("add-note", "widget")
    widget_link = widget_link.replace("http", "https")
    return render_template('add_note.html', form=form, widget_link=widget_link)


@app.route('/widget/')
def widget():
    if len(Note.query.all()) >= 1:
        rand = random.randrange(1, len(Note.query.all()) + 1)
        row = Note.query.filter(Note.id == rand).first().notes
    else:
        row = "No notes in database"
    widget_source = '''/**/document.write('<div class="random-note" style="font-family: Helvetica Neue,Helvetica,Arial,sans-serif; border-radius:4px; background-color:white; border:2px solid #E3E3E3;"> <div class="header" style="background-color: #F5F5F5; padding: 5px; padding-bottom:1px;"><h4 style="margin:0;padding-bottom:3px">Random note is: </h4></div> <div class="body" style="padding: 5px;">''' + row + '''</div></div>');'''  # noqa
    return Response(widget_source, mimetype='application/javascript')


@app.route('/test-widget/')
def test_widget():
    return render_template('test_widget.html')


@app.route('/requests/')
def request_to_app():
    status = request.args.get('status', '')
    if status == 'focused':
        db.session.query(RequestToApp).filter(
            RequestToApp.viewed == False  # noqa
            ).update({RequestToApp.viewed: True})
        db.session.commit()
    selected_requests = RequestToApp.query.order_by(
        RequestToApp.request_time.desc()
        ).limit(10).all()
    return render_template(
        'request_to_app.html',
        selected_requests=selected_requests
        )


@app.route('/requests/table/')
def table():
    requests = RequestToApp.query.order_by(
        RequestToApp.request_time.desc()
        ).limit(10).all()
    data = dict(
        count=RequestToApp.query.filter(
            RequestToApp.viewed == False  # noqa
            ).count(),
        text=render_template('table.html', requests=requests)
    )
    return Response(json.dumps(data), content_type='application/json')


@app.route('/ajax-form/', methods=['GET', 'POST'])
def ajax_form():
    form = NoteForm(request.form, csrf_enabled=False)
    if request.is_xhr and request.method == 'POST':
        if form.validate_on_submit():
            note = form.new_note.data
            if request.files.get('image') is None:
                filename = None
            else:
                image = request.files.get('image')
                filename = ''
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        filename
                    ))
            add_new_note = Note(notes=note, image_path=filename)
            response_data = {}
            try:
                db.session.add(add_new_note)
                db.session.commit()
                response_data['msg'] = u'Your note is now live!'
            except:
                response_data['msg'] = u'Failed to add you note.'
            return Response(
                json.dumps(response_data),
                content_type='application/json'
            )

    return render_template('ajax-form.html', form=form)
