# coding: utf-8
import os
import random
from flask import render_template, redirect, url_for, flash, Response, request

from app import app, db
from app.models import Note
from app.forms import NoteForm


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


@app.route('/add-note', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        add_new_note = Note(notes=form.new_note.data)
        db.session.add(add_new_note)
        db.session.commit()
        flash('Your post is now live!')
    widget_link = request.url.replace("add-note", "widget")
    widget_link = widget_link.replace("http", "https")
    return render_template('add_note.html', form=form, widget_link=widget_link)


@app.route('/widget')
def widget():
    if len(Note.query.all()) >= 1:
        rand = random.randrange(1, len(Note.query.all()) + 1)
        row = Note.query.filter(Note.id == rand).first().notes
    else:
        row = "No notes in database"
    widget_source = '''/**/document.write('<div class="random-note" style="font-family: Helvetica Neue,Helvetica,Arial,sans-serif; border-radius:4px; background-color:white; border:2px solid #E3E3E3;"> <div class="header" style="background-color: #F5F5F5; padding: 5px; padding-bottom:1px;"><h4 style="margin:0;padding-bottom:3px">Random note is: </h4></div> <div class="body" style="padding: 5px;">''' + row + '''</div></div>');'''  # noqa
    return Response(widget_source, mimetype='application/javascript')


@app.route('/test-widget')
def test_widget():
    return render_template('test_widget.html')
