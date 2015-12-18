# coding: utf-8
import os, random
from flask import render_template, redirect, url_for, flash, Response, request

from app import app, db
from app.models import Note
from app.forms import NoteForm


@app.route('/list-notes', methods=['GET', 'POST'])
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
    rand = random.randrange(1, len(Note.query.all()) + 1)
    row = Note.query.filter(Note.id==rand).first()
    # widget_source = '''/**/document.write('<div class=\"rembeddit\" style=\"font-family:verdana,arial,helvetica,sans-serif;background-color: #FFFFFF;border: 1px solid #336699;\" ><div class=\"reddit-header\" style=\"padding: 5px; padding-bottom:1px;background-color:#CEE3F8\" ><h4 class=\"reddit-title\" style=\"margin:0;padding-bottom:3px\" ><a href=\"https://www.reddit.com/\" style=\"margin:5px;\" ><img src=\"https://www.reddit.com/static/spreddit1.gif\" alt=\"\" style=\"border:none\" /></a>ссылки&#32;от&#32;<a style=\"text-decoration:none;color:#336699\" href=\"https://www.reddit.com/\">reddit.com</a></h3></h4></div><div class=\"rembeddit-content\" style=\"padding:5px;\" ><div style=\"margin-left:5px;margin-top:7px;\" ><div class=\"reddit-link even first-half thing id-t3_3x05n3 \"><a href=\"https://www.reddit.com/r/gifs/comments/3x05n3/terminator_dog/\" class=\"reddit-voting-arrows\" target=\"_blank\" style=\"float:left; display:block;\" ><img src=\"https://www.reddit.com/static/widget_arrows.gif\" alt=\"vote\" style=\"border:none;margin-top:3px;\" /></a><div class=\"reddit-entry entry unvoted\" style=\"margin-left: 28px; min-height:32px;\" ><a class=\"reddit-link-title may-blank\" style=\"text-decoration:none;color:#336699;font-size:small;\" href=\"http://i.imgur.com/JI95VOL.gif\" >Terminator Dog</a><br /><small style=\"color:gray;\" ><span class=\"score dislikes\" style=\"display: none;\" >6371 очко</span><span class=\"score unvoted\" >6372 очка</span><span class=\"score likes\" style=\"display: none;\" >6373 очка</span>&#32;|&#32;<a class=\"reddit-comment-link may-blank\" style=\"color:gray\" href=\"https://www.reddit.com/r/gifs/comments/3x05n3/terminator_dog/\">250 комментариев</a></small></div><div class=\"reddit-link-end\" style=\"clear:left; padding:3px;\" ></div></div></div></div></div>');'''
    widget_source = '''/**/document.write('<div class="random-note" style="font-family: Helvetica Neue,Helvetica,Arial,sans-serif; border-radius:4px; background-color:white; border:2px solid #E3E3E3;"> <div class="header" style="background-color: #F5F5F5; padding: 5px; padding-bottom:1px;"><h4 style="margin:0;padding-bottom:3px">Random note is: </h4></div> <div class="body" style="padding: 5px;">''' + row.notes + '''</div></div>');'''
    return Response (widget_source, mimetype='application/javascript')

@app.route('/test-widget')
def test_widget():
    return render_template('test_widget.html')