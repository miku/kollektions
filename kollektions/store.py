#!/usr/bin/env python
# coding: utf-8

import couchdb
import pyelasticsearch

DB_URL  = 'http://0.0.0.0:5984/'
DB_NAME = 'kollektions'
ES_URL  = 'http://127.0.0.1:9200'

def get_store():
    """
    All data goes into one CouchDB database (DB_NAME),
    different kinds of documents are discriminated by 'type'.
    Will create the database if it doesn't exists.
    """
    couch = couchdb.Server(DB_URL)
    try:
        return couch[DB_NAME]
    except couchdb.http.ResourceNotFound, not_found:
        return couch.create(DB_NAME)

# implement queries abstractions here