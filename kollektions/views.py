#!/usr/bin/env python
# coding: utf-8

from kollektions import app
from kollektions.forms import LoginForm, SignupForm
from kollektions.store import get_store, get_user
from kollektions.utils import calculate_sha1
from flask import render_template, flash, redirect, url_for, session
import pyes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        session['user'] = get_user(form.data['login'])
        return redirect(url_for("index"))    
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

        store = get_store()
        doc_id, doc_rev = store.save({
            'type' : 'user', 
            'email' : __email,
            'username' : __username,
            'password' : calculate_sha1(__pw)})

        session['user'] = store[doc_id]

        return redirect(url_for("index"))    
    return render_template('signup.html', form=form)
