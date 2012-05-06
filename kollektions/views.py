#!/usr/bin/env python
# coding: utf-8

from kollektions import app, db, User
from kollektions.forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for, session, abort, request, jsonify
from functools import wraps
from sqlalchemy import or_

import urllib2
import simplejson

def get_book(id, bibkey = "ISBN"):
    '''Get a Book by its ID: ISBN (default), LCCN, OCLC
    or OLID (Open Library ID).
    
    Returns:
        A pyobj.
    '''
    url = urllib2.urlopen("http://openlibrary.org/api/books?bibkeys=%s:%s&jscmd=data&format=json" % (bibkey, id))
    data = simplejson.load(url)['%s:%s' % (bibkey, id)]
    return data

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not 'user' in session or session['user'] == None:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return decorated_view

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        session['user'] = User.query.filter(or_(User.username==form.data['login'], User.email==form.data['login'])).first()
        return redirect(url_for("home", id=session['user'].id))    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(csrf_enabled=False)
    if form.validate_on_submit():

        __email = form.data['email']
        __username = form.data['username']
        __pw = form.data['password']

        # craete User
        __user = User(username=__username, email=__email, password=__pw)
        db.session.add(__user)
        db.session.commit()

        # save and get the id for retrieval
        id = __user.id
        # query the new user, since u is detached here
        user = User.query.get(id)

        # authenticated
        session['user'] = user

        return redirect(url_for("home", id=user.id))
    return render_template('signup.html', form=form)

@app.route('/users/<int:id>/')
@login_required
def home(id):
    user = User.query.get(id)
    if user == None:
        return abort(404)
    if not session['user'].id == user.id:
        return abort(403)
    return render_template('home.html', user=user)

@app.route('/api/v1/books', methods=['PUT'])
def api_books_put():
    """ 
    add a new book by isbn
    """
    try:
        apikey = request.form['key']
        isbn = request.form['isbn']
    except KeyError:
        response = jsonify(status='400', message='key and isbn parameters are required')
        response.code = 400
        return response

    user = User.query.filter(User.apikey==apikey).first()
    if user == None:
        response = jsonify(apikey=apikey, isbn=isbn, status='400', message='user not found')
        response.code = 400
        return response

    try:
        metadata = get_book(isbn)
    except KeyError:
        response = jsonify(apikey=apikey, isbn=isbn, status='404', message='book with this ISBN not found')
        response.code = 404
        return response

    # get book info by isbn ...
    # return data gathered and stored
    return jsonify(key=apikey, status='200', isbn=isbn, message='OK', metadata=metadata)
