#!/usr/bin/env python
# coding: utf-8

import couchdb
import pyelasticsearch
from kollektions import app

def get_store():
    """
    All data goes into one CouchDB database (DB_NAME),
    different kinds of documents are discriminated by 'type'.
    Will create the database if it doesn't exists.
    """
    couch = couchdb.Server(app.config['COUCHDB_URL'])
    try:
        return couch[DB_NAME]
    except couchdb.http.ResourceNotFound, not_found:
        return couch.create(app.config['COUCHDB_NAME'])

# implement queries abstractions here