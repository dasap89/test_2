import os
from flask import render_template, redirect, url_for, flash

from app import app, db
from app.models import Note
from app.forms import NoteForm


@app.route('/list-notes', methods = ['GET', 'POST'])
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

@app.route('/add-note', methods = ['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        add_new_note = Note(notes=form.new_note.data)
        db.session.add(add_new_note)
        db.session.commit()
        flash('Your post is now live!')
    return render_template('add_note.html', form=form )
