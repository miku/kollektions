#!/usr/bin/env python
# coding: utf-8

from kollektions import app, db, User
from kollektions.forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for, session, abort
from functools import wraps
from sqlalchemy import or_

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not 'user' in session:
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
    print(session)
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
    if not session['user'].id == user.id:
        return abort(403)
    if user == None:
        return abort(404)
    return render_template('home.html', user=user)
