#!/usr/bin/env python
# coding: utf-8

from kollektions import app
from kollektions.forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(csrf_enabled=False)
	if form.validate_on_submit():
		return redirect(url_for("index"))    
	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm(csrf_enabled=False)
	if form.validate_on_submit():
		return redirect(url_for("index"))    
	return render_template('signup.html', form=form)
