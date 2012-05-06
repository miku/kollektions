#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Kollektions')
    parser.add_argument('-s', '--server', metavar='SERVER', type=str,
        default='development', help='server setup, one of [development, gevent]')
    parser.add_argument('--create-db', action='store_true', help='create users db')

    args = parser.parse_args()

    # create the user, event and followers table 
    # (by default as sqlite3 in /tmp/kollektions.db)
    # you can override this setting in kollektions/__init__.py
    if args.create_db:
        from kollektions import db
        db.create_all()
        sys.exit(0)

    # start server (default: development, production: gevent)
    if args.server == 'development':
        from kollektions import app
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = '0913547b7f5db1c55094f5238d666c4d'

        # our own config (sql db config, see: kollektions/__init__.py)
        app.config['COUCHDB_URL'] = 'http://0.0.0.0:5984/'
        app.config['COUCHDB_NAME'] = 'kollektions'
        app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200'

        app.run(host='0.0.0.0', debug=True)

    elif args.server == 'gevent':
        try:
            from gevent.wsgi import WSGIServer
        except ImportError:
            print('please install gevent / libevent')
            print('this is just a production server option, to run development server')
            print('just use ')
            print
            print('    $ python runserver.py')
            print
            sys.exit(1)

        from kollektions import app

        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = '0913547b7f5db1c55094f5238d666c4d'

        # our own config (sql db config, see: kollektions/__init__.py)
        app.config['COUCHDB_URL'] = 'http://0.0.0.0:5984/'
        app.config['COUCHDB_NAME'] = 'kollektions'
        app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200'
        
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
