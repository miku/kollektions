#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

# setup db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# database is used just for users and social streams
class User(db.Model):
    """
    An application user profile with minimal information.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    apikey = db.Column(db.String(36))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.apikey = str(uuid.uuid4())

    def __repr__(self):
        return '<User %r>' % self.username

class Event(db.Model):
    """
    An event to display in the user's newsfeed.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event = db.Column(db.Unicode(1024))
    time = db.Column(db.Integer) # unix timestamp
    data = db.Column(db.BLOB())
   
    def __init__(self, user_id=None, event=None, time=None, data=None):
        self.user_id = user_id
        self.event = event
        self.time = time
        self.data = data

    def __repr__(self):
        return '<Event %r>' % self.id

class Following(db.Model):
    """
    Social network DNA, twitter style.
    """
    user_id = db.Column(db.Integer, primary_key=True)
    following_user_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id=None, following_user_id=None):
        self.user_id = user_id
        self.following_user_id = following_user_id

    def __repr__(self):
        return '<Following %r -> %r>' % (self.user_id, self.following_user_id)

import kollektions.views

