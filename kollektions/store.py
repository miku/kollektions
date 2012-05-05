#!/usr/bin/env python
# coding: utf-8

import couchdb
import pyes

DB_URL  = 'http://0.0.0.0:5984/'
DB_NAME = 'kollektions'
ES_URL  = '127.0.0.1:9200'

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

def get_user_by_email(email):
    """
    Return a user (dict) or none, if the user doesn't exist.
    """
    user, conn = None, pyes.ES(ES_URL)

    q = pyes.query.TermQuery('email', email)
    resultset = conn.search(query=q, indices='kollektions')
    print(resultset)
    if len(resultset['hits']['hits']) == 1:
        user = resultset['hits']['hits'][0]['_source']

    return user

def get_user_by_username(username):
    """
    Return a user (dict) or none, if the user doesn't exist.
    """
    user, conn = None, pyes.ES(ES_URL)

    q = pyes.query.TermQuery('username', username)
    resultset = conn.search(query=q, indices='kollektions')
    if len(resultset['hits']['hits']) == 1:
        user = resultset['hits']['hits'][0]['_source']

    return user

def get_user_by_username_or_email(username_or_email):
    """
    Fuzzy lookup, used for 'login with your username *or* email' login page.
    """
    print(get_user_by_username(username_or_email))
    print(get_user_by_email(username_or_email))
    return (
        get_user_by_username(username_or_email) or 
        get_user_by_email(username_or_email)
    )
