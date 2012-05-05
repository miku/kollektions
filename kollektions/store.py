#!/usr/bin/env python
# coding: utf-8

import couchdb
import pyes

DB_URL = 'http://0.0.0.0:5984/'
DB_NAME = 'kollektions'

def get_store():
    couch = couchdb.Server(DB_URL)
    try:
        return couch[DB_NAME]
    except couchdb.http.ResourceNotFound, not_found:
        __user_db = couch.create(DB_NAME)
        return __user_db

def get_user(username_or_email):
    conn = pyes.ES('127.0.0.1:9200')
    
    q = pyes.query.FieldQuery(pyes.query.FieldParameter("username", username_or_email))
    resultset = conn.search(query=q, indices='kollektions')

    # try email, too
    if len(resultset['hits']['hits']) == 0:
        q = pyes.query.FieldQuery(pyes.query.FieldParameter("email", username_or_email))
        resultset = conn.search(query=q, indices='kollektions')
        if len(resultset['hits']['hits']) == 1:
            return resultset['hits']['hits'][0]['_source']
    elif len(resultset['hits']['hits']) == 1:
        return resultset['hits']['hits'][0]['_source']

    return None
