#!/usr/bin/env python
# coding: utf-8

from kollektions import app, db, User, Event, Following
from kollektions.forms import LoginForm, SignupForm
from kollektions.store import get_store
from kollektions.utils import pretty_date
from flask import render_template, flash, redirect, url_for, session, abort, request, jsonify
from functools import wraps
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError

import couchdb
import time
import datetime
import urllib2
try:
    import simplejson as json
except ImportError:
    import json
import pyelasticsearch

def get_book(id, bibkey = "ISBN"):
    '''Get a Book by its ID: ISBN (default), LCCN, OCLC
    or OLID (Open Library ID).
    
    Returns:
        A pyobj.
    '''
    url = urllib2.urlopen("http://openlibrary.org/api/books?bibkeys=%s:%s&jscmd=data&format=json" % (bibkey, id))
    data = json.load(url)['%s:%s' % (bibkey, id)]
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
def home(id):
    user = User.query.get(id)
    if user == None:
        return abort(404)
    # if not session['user'].id == user.id:
    #     return abort(403)

    # __events = Event.query.filter(Event.user_id==user.id).order_by('-time')
    followed = Following.query.filter(Following.user_id==user.id).all()
    event_user_ids = [ f.following_user_id for f in followed ] + [user.id]
    __events = Event.query.filter(Event.user_id.in_(event_user_ids)).order_by('-time')

    events = []

    event_map = {
        'book added' : 'added',
        'book deleted' : 'removed'
    }

    for event in __events:
        event_data = json.loads(event.data)
        try:
            e = { 
                'user_id' : event.user_id,
                'username' : User.query.get(event.user_id).username,
                'title' : event_data['metadata']['title'],
                'doc_id' : event_data['doc_id'],
                # 'time' : datetime.datetime.fromtimestamp(event.time).strftime('%d.%m.%Y %H:%M'),
                'time' : pretty_date(datetime.datetime.fromtimestamp(event.time)),
                'action' : event_map[event.event],
            }
            events.append(e)
        except Exception as exc:
            # print(exc)
            pass # be graceful

    # following
    if 'user' in session:
        following = bool(Following.query.filter(and_(
            Following.user_id==session['user'].id, 
            Following.following_user_id==user.id)).first())

    return render_template('home.html', user=user, events=events, following=following)

@app.route('/add', methods=['POST'])
@login_required
def add():
    try:
        isbn = request.form['isbn']
    except KeyError:
        abort(404)

    user = session['user']
    if user == None:
        abort(404)

    try:
        metadata = get_book(isbn)
    except KeyError:
        flash('ISBN not found')
        return redirect(url_for('home', id=user.id))

    # see if user already got this books stored
    conn = pyelasticsearch.ElasticSearch('http://localhost:9200/')
    results = conn.search("%s AND user_id:%s" % (isbn, user.id))
    if len(results['hits']['hits']) > 0:
        metadata = results['hits']['hits'][0]['_source']['metadata']
        doc_id = results['hits']['hits'][0]['_source']['_id']
        return jsonify(key=apikey, status='200', isbn=isbn, message='OK', metadata=metadata, doc_id=doc_id)

    # if not found, store it in CouchDB
    store = get_store()

    doc = {
        "user_id" : user.id,
        "metadata" : metadata
    }
    doc_id, doc_rev = store.save(doc)

    # add to social stream
    event = Event(user_id=user.id, event='book added', time=time.time(),
        data=json.dumps({
            "verbose" : "%s added %s to their collection" % (user.username, metadata['title']),
            "metadata" : metadata,
            "doc_id" : doc_id,
        }))
    db.session.add(event)
    db.session.commit()

    flash('Successfully added book')
    return redirect(url_for('home', id=user.id))

@app.route('/follow/<id>')
@login_required
def follow(id):
    user = session['user']
    if user == None:
        abort(404)

    followed = User.query.get(id)
    if followed == None:
        abort(404)

    if followed.id == user.id:
        # don't follow self
        return redirect(url_for('home', id=followed.id))

    try:
        following = Following(user_id=user.id, following_user_id=followed.id)
        db.session.add(following)
        db.session.commit()
    except IntegrityError as ie:
        # already followed
        db.session.rollback()

    return redirect(url_for('home', id=followed.id))    

@app.route('/unfollow/<id>')
@login_required
def unfollow(id):
    user = session['user']
    if user == None:
        abort(404)

    followed = User.query.get(id)
    if followed == None:
        abort(404)

    if followed.id == user.id:
        # don't follow self
        return redirect(url_for('home', id=followed.id))

    try:
        following = Following.query.filter(and_(
            Following.user_id==session['user'].id, 
            Following.following_user_id==followed.id)).first()
        if not following == None:
            db.session.delete(following)
            db.session.commit()
    except Exception as exc:
        db.session.rollback()

    return redirect(url_for('home', id=followed.id))    


@app.route('/item/<id>')
def item(id):
    store = get_store()
    try:
        doc = store[id]
    except couchdb.http.ResourceNotFound, not_found:
        return abort(404)

    user = User.query.get(doc['user_id'])
    return render_template('item.html', doc=doc, user=user)


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
        response = jsonify(apikey=apikey, status='400', message='user not found')
        response.code = 400
        return response

    try:
        metadata = get_book(isbn)
    except KeyError:
        response = jsonify(apikey=apikey, isbn=isbn, status='404', message='book with this ISBN not found')
        response.code = 404
        return response

    # see if user already got this books stored
    conn = pyelasticsearch.ElasticSearch('http://localhost:9200/')
    results = conn.search("%s AND user_id:%s" % (isbn, user.id))
    if len(results['hits']['hits']) > 0:
        metadata = results['hits']['hits'][0]['_source']['metadata']
        doc_id = results['hits']['hits'][0]['_source']['_id']
        return jsonify(key=apikey, status='200', isbn=isbn, message='OK', metadata=metadata, doc_id=doc_id)

    # if not found, store it in CouchDB
    store = get_store()

    doc = {
        "user_id" : user.id,
        "metadata" : metadata
    }
    doc_id, doc_rev = store.save(doc)

    # add to social stream
    event = Event(user_id=user.id, event='book added', time=time.time(),
        data=json.dumps({
            "verbose" : "%s added %s to their collection" % (user.username, metadata['title']),
            "metadata" : metadata,
            "doc_id" : doc_id,
        }))
    db.session.add(event)
    db.session.commit()

    # get book info by isbn ...
    # return data gathered and stored
    return jsonify(key=apikey, status='200', isbn=isbn, message='OK', metadata=metadata, doc_id=doc_id)


@app.route('/api/v1/books', methods=['DELETE'])
def api_books_delete():
    """ 
    delete book by internal id (couchdb doc_id)
    """
    try:
        apikey = request.args.get('key', None)
        doc_id = request.args.get('id', None) # doc id
    except KeyError:
        response = jsonify(status='400', message='key and id parameters are required')
        response.code = 400
        return response

    user = User.query.filter(User.apikey==apikey).first()
    if user == None:
        response = jsonify(apikey=apikey, status='400', message='user not found')
        response.code = 400
        return response

    # remove book from couchdb
    try:
        store = get_store()
        doc = store[doc_id]
        metadata = doc['metadata']
        store.delete(doc)
    except couchdb.http.ResourceNotFound, not_found:
        return jsonify(key=apikey, status='200', message='OK')

    # add to social stream
    event = Event(user_id=user.id, event='book deleted', time=time.time(),
        data=json.dumps({"verbose" : "%s removed %s from their collection" % (user.username, metadata['title']) }))
    db.session.add(event)
    db.session.commit()

    # get book info by isbn ...
    # return data gathered and stored
    return jsonify(key=apikey, status='200', message='OK')

@app.route('/api/v1/books', methods=['GET'])
def api_books_get():
    try:
        apikey = request.args.get('key', None)
    except KeyError:
        response = jsonify(status='400', message='key parameter is required')
        response.code = 400
        return response

    user = User.query.filter(User.apikey==apikey).first()
    if user == None:
        response = jsonify(apikey=apikey, status='400', message='user not found')
        response.code = 400
        return response

    conn = pyelasticsearch.ElasticSearch('http://localhost:9200/')
    results = conn.search("user_id:%s" % user.id)

    payload = []

    for result in results['hits']['hits']:
        item = {}
        md = result['_source']['metadata']
        item = {'title' : md['title'], 'id' : result['_source']['_id'] }
        try:
            item.update({'authors' : md['authors']})
        except KeyError:
            pass
        payload.append(item)

    return jsonify(key=apikey, status='200', message='OK', items=payload, count=len(results['hits']['hits']))

