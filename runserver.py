#!/usr/bin/env python
# coding: utf-8

import argparse
import pyes
import sys

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Kollektions')
    parser.add_argument('-s', '--server', metavar='SERVER', type=str,
        default='development', help='server setup, one of [development, gevent]')
    parser.add_argument('--ping', action='store_true', help='ping couchdb')

    args = parser.parse_args()

    # count the #docs in couchdb
    if args.ping:
        from kollektions.store import get_store, DB_URL, DB_NAME
        __store = get_store()
        print('%s docs in store (%s, %s)' % (len(__store), DB_URL, DB_NAME))
        sys.exit(0)

    # start server (default: development, production: gevent)
    if args.server == 'development':
        from kollektions import app
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = '0913547b7f5db1c55094f5238d666c4d'
        app.run(host='0.0.0.0', debug=True)

    elif args.server == 'gevent':
        from gevent.wsgi import WSGIServer
        from kollektions import app

        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = '0913547b7f5db1c55094f5238d666c4d'

        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
