#!/usr/bin/env python
# coding: utf-8

from kollektions import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

